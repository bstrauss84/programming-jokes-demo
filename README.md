# Sample 'Programming Jokes' Application Deployment and Update Guide on OpenShift

This README provides a comprehensive guide on deploying a simple Flask application, which serves extremely cheesy and randomly selected programming jokes, on OpenShift, and also outlines how to update the application with new content and versioning.

## Prerequisites

- Access to an OpenShift cluster
- OpenShift CLI (`oc`) installed
- Podman or Docker installed
- Git installed

## Initial Setup

### Log Into Your OpenShift Cluster

Authenticate via CLI:

```bash
oc login --token=<your-token> --server=<your-cluster-api-url>
```

### Expose the Internal OpenShift Registry

Ensure the internal registry is externally accessible:

```bash
oc patch configs.imageregistry.operator.openshift.io/cluster --patch '{"spec":{"defaultRoute":true}}' --type=merge
```

### Clone the Repository

Clone the application's repository:

```bash
git clone https://github.com/bstrauss84/programming-jokes-demo.git
cd ./programming-jokes-demo
```

### Define Environment Variables

To simplify the rest of this excercise, let's go ahead and define some environment variables for our OpenShift internal registry route, as well as the namespace, and initial image tag for our sample application:

```bash
OPENSHIFT_REGISTRY_ROUTE=$(oc get route default-route -n openshift-image-registry --template='{{ .spec.host }}')
NAMESPACE="demo-$(oc whoami)"
```

## Application Structure

- **`app.py`**: The main Flask application file containing the server logic and joke list.
- **`requirements.txt`**: Specifies Python package dependencies for the application.
- **`templates/index.html`**: HTML template for rendering the jokes in a web browser.
- **`Containerfile`**: Used to build the container image of the application.

## Deploying the Application

### Build the Container Image

Build your image using Podman or Docker:

```bash
podman build -t $OPENSHIFT_REGISTRY_ROUTE/$NAMESPACE/programming-jokes:latest .
```

### Tag and Push the Image to the OpenShift Registry

Authenticate with the OpenShift registry:

```bash
podman login -u $(oc whoami) -p $(oc whoami -t) $OPENSHIFT_REGISTRY_ROUTE
```

Push your image to the internal OpenShift registry:

```bash
podman push $OPENSHIFT_REGISTRY_ROUTE/$NAMESPACE/programming-jokes:latest
```

### Deploy and Expose the Application

Deploy your application on OpenShift:

```bash
oc new-project $NAMESPACE
oc new-app $NAMESPACE/programming-jokes:latest --name=programming-jokes-app
oc create route edge programming-jokes-app --service=programming-jokes-app --insecure-policy=Redirect
```

## Accessing Your Deployed Application

After deploying your application and exposing it via a route, you can easily find the URL to access it with the following command:

```bash
echo "Application URL: https://$(oc get route programming-jokes-app -o jsonpath='{.spec.host}')"
```

### Next Steps:

1. **Navigate to the Application URL**: Open a web browser and go to the URL output by the previous command.
2. **Explore the Application**: Click the "Get Another Joke" button a few times to see different programming jokes displayed. This verifies that your application is running successfully and serving content dynamically.

## Updating the Application

To update your application (e.g., adding new jokes), follow these steps:

1. **Edit `app.py`**: 

   Add a new joke to the end of the joke list.  For example...

   ```python
   "I've been using Vim for a long time now, mainly because I can't figure out how to exit it."
   ```

**IMPORTANT:** Remember, when adding a new joke, ensure you place a comma at the end of the preceding line to maintain valid Python list syntax.

2. **(Optional) Update the Containerfile**:

   Modify the ENV variable `APP_VERSION` in the Containerfile from `1.0` to `2.0`.


3. **Rebuild and Push the Updated Image**:

   Rebuild the image with the new content:
   ```bash
   podman build -t $OPENSHIFT_REGISTRY_ROUTE/$NAMESPACE/programming-jokes:latest .
   ```

   Push the updated image to the registry:
   ```bash
   podman push $OPENSHIFT_REGISTRY_ROUTE/$NAMESPACE/programming-jokes:latest
   ```

## Verifying Application Updates

Ensure the deployment has rolled out the new version:

   ```bash
   oc rollout status deployment/programming-jokes-app
   oc get pods -n $NAMESPACE
   ```

After updating your application, pushing the new image, and ensuring your deployment is using this latest version, repeat the process to access your application:

```bash
echo "Application URL: https://$(oc get route programming-jokes-app -o jsonpath='{.spec.host}')"
```

### Next Steps:

1. **Visit the Application Again**: Use the URL provided by the command to open your application in a web browser.
2. **Check for New Content**: Press the "Get Another Joke" button multiple times until you see the new jokes appear. This confirms that the update was successful and the new version of your application is live.  If you did the optional step earlier, where you updated the Containerfile, you should notice that the "**Current Version:**" listed beneath the button has been updated as well.

![Updated Application](https://github.com/bstrauss84/programming-jokes-demo/blob/main/content/updated_application.png?raw=true)

## Conclusion

This guide walked us through the process of deploying a simple Flask application on OpenShift, making updates to the application, and managing deployment updates. It covered everything from initial setup to deploying and updating the application.

## THE END
