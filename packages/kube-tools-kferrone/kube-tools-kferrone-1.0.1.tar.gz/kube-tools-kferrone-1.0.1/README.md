# Kube Tools  

A useful set of kustomize and kubectl tools for improving the kubectl experience. 

## Requirements  

 - [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
 - [kustomize](https://kubectl.docs.kubernetes.io/installation/kustomize/)
 - [helm](https://helm.sh/docs/intro/install/)
 - [krew](https://krew.sigs.k8s.io/docs/user-guide/setup/install/)

### Configure `kubectl`, `kustomize`, and `helm`  

Now we want to set up our environment for kustomize, kubectl, and helm to use this project as the working directory simply by exporting `XDG_CONFIG_HOME` and adding the kubectl plugins to the `PATH`.  

`~/.bash_profile`  
```sh
export XDG_CONFIG_HOME="path/to/home_cluster"
export PATH=$PATH:$XDG_CONFIG_HOME/kubectl/plugin
```  
Here is what's going on:  
 - `kustomize` is looking for `$XDG_CONFIG_HOME/kustomize/plugin`
 - `kubectl` is looking for executables on the `PATH` which start with `kubectl-`, e.g. `kubectl-myplugin`. This is why we add the `/kubectl/plugin` dir to the path. 
 - `helm` is looking to create a working dir at `$XDG_CONFIG_HOME/helm`. 