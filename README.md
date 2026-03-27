# Smart Fridge

A cloud-native application with backend, frontend, and notifier services, deployable to AWS EKS using Helm and managed by ArgoCD.

## Prerequisites

- AWS CLI configured with access to your EKS cluster
- kubectl installed and configured
- Helm installed
- ArgoCD installed and configured
- Docker (for local builds/testing)

## Local Development (Docker Compose)

```sh
docker-compose up --build
```
- Backend: http://localhost:5000
- Frontend: http://localhost:8080

## Kubernetes Deployment (AWS EKS + ArgoCD)

### 1. Build and Push Docker Images (if needed)

Update the image tags in `fridge-app/values.yaml` if you build new images.

### 2. Update values.yaml

Set the correct image repositories and tags, and ensure:
```yaml
frontend:
  containerPort: 80
  servicePort: 80
backend:
  containerPort: 5000
  servicePort: 5000
serviceType: LoadBalancer
```

### 3. Configure ArgoCD Application

Edit `k8s/argocd-app.yaml`:
```yaml
spec:
  destination:
    server: https://<your-eks-api-endpoint>
    namespace: <your-namespace>
```
- Find your EKS API endpoint in the AWS console under EKS > Clusters > Overview.

### 4. Apply ArgoCD Application

```sh
kubectl apply -f k8s/argocd-app.yaml
```

### 5. Sync in ArgoCD UI

- Open ArgoCD UI.
- Sync the `fridge-app` application.

### 6. Verify Deployment

```sh
kubectl get pods
kubectl get svc
```
- Note the EXTERNAL-IP for backend and frontend services.

### 7. Access the Application

- Frontend: http://<EXTERNAL-IP>
- Backend: http://<EXTERNAL-IP>:5000 (or as configured)

## Cleanup (Kubernetes)

To remove all resources deployed by this project:

```sh
kubectl delete -f k8s/argocd-app.yaml
# Optionally, delete Helm releases and namespaces if used:
# helm uninstall <release-name> -n <namespace>
# kubectl delete namespace <namespace>
```

## Troubleshooting

- If LoadBalancer is not working, ensure your security group allows inbound traffic on the correct ports (80, 5000, etc.).
- If AWS EKS console does not show pods/namespaces, ensure your IAM user/role is added to the `aws-auth` ConfigMap with `system:masters` group.
- If health checks fail, ensure your services and containers are listening on the correct ports (Nginx default is 80).

## Useful Commands

- List ArgoCD apps: `argocd app list`
- Get ArgoCD app status: `argocd app get fridge-app`
- Get pods: `kubectl get pods`
- Get services: `kubectl get svc`
- View logs: `kubectl logs <pod-name>`

## IAM Access for EKS Console

Add your IAM user to the `aws-auth` ConfigMap:
```yaml
mapUsers: |
  - userarn: arn:aws:iam::<your-account-id>:user/<your-iam-username>
    username: <your-iam-username>
    groups:
      - system:masters
```
Apply with:
```sh
kubectl -n kube-system apply -f aws-auth.yaml
```
