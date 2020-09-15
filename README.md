# Metrics Dashboard

## A _[Software and Systems Laboratory](https://ssl.cs.luc.edu/metrics_dashboard.html)_ Project

### **How It Works**

Using the [GitHub API](https://developer.github.com/v3/) we gather information about a repository, and use [pandas](https://pandas.pydata.org/) to display the information.

---

## Module Development

### **Creating a Compatible Project Module**

---

1. Create a folder for your module following the folder structure of `module_template`.

    * This folder is the root folder of your module.

2. Create a subfolder called `code` within your the root folder of your module.

3. Inside the `code` folder, place all of your Python code for your module.

    * For each library you import from PIP in **ANY** of your Python code, add the library name to a `requirements.txt` file within the `code` folder.

4. Copy the `Dockerfile` from the `module_template` folder into root folder of your module.

    * Depending how your files are named, the `ENTRYPOINT` command of the `Dockerfile` might need to be changed.

## Running Modules

### **How to Run a Module**

---

0. Ensure that Docker is installed and can be executed via the terminal.

1. `cd` into a module.

2. Run `docker build -t <IMAGE_NAME> .`.

    * Replace `<IMAGE_NAME>` with the image name of the module being ran.

        * This image name can be anything as long as it is memorable

    * This will create a Docker container with the image name `<IMAGE_NAME>`.

3. To run the module, run `docker run <IMAGE_NAME> <GITHUB_URL> <PERSONAL_ACCESS_TOKEN>`

    * Replace `<GITHUB_URL>` with a `https://github.com/<USERNAME>/<REPOSITORY>` URL.

    * Replace `<PERSONAL_ACCESS_TOKEN>` with you GitHub account [Personal Account Token](https://github.com/settings/tokens)

        * This token needs to have access only to the _**repo** : Full Control of Private Repositories_ scope.

### **How to Run the Example Module**

---

0. Ensure that Docker is installed and can be executed via the terminal.

1. `cd` into the `module_template` folder.

2. Run `docker build -t template .`.

3. To run the module, run `docker run template <WORD>

    * Replace `<WORD>` with whatever string you want printed to the console.

        * This is meant to show how to pass arguements from Docker to a Python script.

    * This container also prints the results of a basic HTTP GET request

        * This utilizes the [requests library](https://requests.readthedocs.io/en/master/) to serve as an example library import in a `requirements.txt`.

4. The result should look like this:

        Hello, World!
        Your first command line argument is:
        word
        {'userId': 1, 'id': 1, 'title': 'delectus aut autem', 'completed': False}

## File Sharing from Docker Containers to Host Machines

### **Windows Instructions**

---

To share files between your computer and your Docker containers, you need to create a volume. This should be pretty simple on *nix machines - I haven't had a chance to test on Mac/Linux, but I have been able to make it work on Windows, which is a more complicated process.

First, assuming you are not on an enterprise version of Windows and therefore you are using Docker Toolbox with Oracle VirtualBox, you will need to create a "Shared Folder".

I suggest following this [tutorial](http://support.divio.com/en/articles/646695-how-to-use-a-directory-outside-c-users-with-docker-toolbox-docker-for-windows) and changing all instances of "Divio" in the commands to "metrics-vol" or something else you recognize:

The second part of this process, as mentioned in the tutorial, is permanently mounting the new shared folder in your default Docker machine. The tutorial provides good instructions on how to do this, and I will note that one way to edit the `profile` document is to use the default Linux `echo` command. First do a `sudo su` to give yourself proper permissions, then run `echo -e '\nsudo mkdir /metrics-vol\nsudo mount -t vboxsf -o uid=1000,gid=50 metrics-vol /metrics-vol' >> profile`.

After following the tutorial above as described, you should be able to read and write files in the shared folder you set up on your host machine from your Docker containers at the path `/metrics-vol`, so long as you mount a volume when you run the container. This command should look like `docker run -v /metrics-vol:/metrics-vol image-name command_line_argument`
I've included some test code in module_template/app.py that is currently commented out - if you correctly add a shared folder on your host machine, mount the folder on your default Docker machine, and mount it as a volume when you run the container (after building the image with the lines uncommented), it should write your command line argument
to a file called `voltest.txt` that exists in your shared folder on your host machine.

### **Mac/ Linux Instructions**

---

0. Ensure that the Docker container that you want the data from is dead

1. Run `docker volume create <VOLUME_NAME>`

    * Replace `<VOLUME_NAME>` with the name of the volume being created.

        * This volume name can be anything as long as it is memorable

    * This will create a Docker volume with the name `<VOLUME_NAME>`.

2. Create a Docker container as described [earlier in this README.md](#how-to-run-a-module).

3. Run `docker run -v <VOLUME_NAME>:/<VOLUME_NAME> <IMAGE_NAME> <GITHUB_URL> <PERSONAL_ACCESS_TOKEN>`

    * For an understanding of what `<GITHUB_URL>` and `<PERSONAL_ACCESS_TOKEN>` are, refer to [earlier in this README.md](#how-to-run-a-module).

#### _After the Container has Completed its Task_

4. Run `docker container ls -a` and copy the Container ID (`<CONTAINER_ID>`) of the Container whose Image Name is the same as `<IMAGE_NAME>`.

5. Run `docker cp <CONTAINER_ID>:/<VOLUME_NAME> <HOST_PATH>`

    * `<HOST_PATH>` is the path where data will be exported to on the HOST MACHINE.

#### **Running FE Flask Server to Display Data**

`docker run -v metrics:/metrics -p 5000:5000 <name_of_image>`

#### **Running the script to run everything**

To run the scripts, run the following commands while in the top SSLMetrics directory:

`chmod +x ./all_metrics.sh`

`chmod +x ./Commits/metrics.sh`

`chmod +x ./Issues/metrics.sh`

`chmod +x ./Lines_Of_Code_Num_Of_Chars/metrics.sh`

`chmod +x ./Issue_Spoilage/metrics.sh`

`chmod +x ./Defect_Density/metrics.sh`

`./all_metrics.sh github.com/<owner>/<repo_name> <api_token>`

_Note: the chmod commands need to be run only initially. After that, just run the all_metrics.sh script with the GitHub repo as the command line argument._
