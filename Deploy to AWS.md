# Deployment using AWS EC2

Before following further instructions, make sure you have tried running the Python Bot locally first. You also need to have an AWS account before deploying.

# Table of Contents

- [Deployment using AWS EC2](#deployment-using-aws-ec2)
- [Table of Contents](#table-of-contents)
- [Why AWS EC2?](#why-aws-ec2)
- [How to Use AWS EC2](#how-to-use-aws-ec2)
  - [Create EC2 Instance](#create-ec2-instance)
  - [Access EC2 Instance Using SSH](#access-ec2-instance-using-ssh)
  - [Install Python, Pip and Git on EC2 Instance](#install-python-pip-and-git-on-ec2-instance)
  - [Clone Source Code from GitHub](#clone-source-code-from-github)
  - [Create a Virtual Environment and Install Dependencies](#create-a-virtual-environment-and-install-dependencies)
  - [Setting up configuration](#setting-up-configuration)
  - [Running a Python Bot](#running-a-python-bot)
  - [Tips: Keeping the Bot Running](#tips-keeping-the-bot-running)

# Why AWS EC2?

Provides free services for light usage for 1 year (AWS Free Tier). It is very flexible and suitable for more complex projects. Open the [link](https://aws.amazon.com/ec2) to register.

# How to Use AWS EC2

The following are the steps to use AWS EC2 and run Python source code from GitHub on that server. Make sure you have an AWS account and are logged in.

## Create EC2 Instance

Note: We will use the Free Tier only.

1. Open the **[AWS Management Console](https://console.aws.amazon.com/)**.

2. Navigate to the **EC2** service by searching for it in the **Services** menu (next to the AWS logo).

3. Click **Launch Instance**.

4. **Configure Instance**:

   - Name the instance (e.g. `MyPythonServer`).

   - Select an **Amazon Machine Image (AMI)**:

     - Select **Ubuntu Server 22.04 LTS (HVM), SSD Volume Type**.

   - Select an **Instance Type**:

     - Select **t2.micro**.

5. **Configure Key Pair**:

   - Create a new key pair by pressing **Create new key pair**.

   - Give it a name, for example `my-key-pair`.

   - Choose the key file format:

     - If you are going to connect with OpenSSH, choose `.pem`.

     - If you will connect with PuTTY (for Windows), select `.ppk`.

   - Save the file by pressing **Create key pair**.

6. **Configure Network Settings**:

   - Check **Allow SSH traffic from** and change it to **My IP** (for security) or leave it as Anywhere `0.0.0.0/0` (to be accessible from anywhere). Avoid selecting `0.0.0.0/0` (access from all IPs), unless absolutely necessary.

7. **Configure Storage**:

   - Ensure that the storage allocation is sufficient for your project needs. 8 GB is usually enough for small applications.

8. (**Optional**) Install dependencies (`pip install` for Python scripts). In the **Advanced Details** section, find **User Data (for bootstrapping)** and add the code below in the input field.
   ```bash
   #!/bin/bash
   sudo apt-get update
   sudo apt-get install -y python3-pip
   pip3 install -r /home/ubuntu/requirements.txt
   ```

9. Click **Launch Instance**.

## Access EC2 Instance Using SSH

1. Navigate to the **Instances** tab in the **EC2 Console** and select your instance, click the **Connect** button, select the **SSH client** menu. Copy the SSH command example.

2. Open a terminal on your computer and access the instance using SSH, paste the SSH command above.

   - Change the location of the `.pem` file according to the location of the file you saved.

   - If there is an error regarding permissions, run command below.
     ```bash
     chmod 400 /path/to/my-key-pair.pem
     ```
     Then try making a connection again using SSH.

3. (**Optional**) If an error occurs while making the connection and you are tired, please use **CloudShell** which is located in the bottom left corner or in the top menu with the console icon next to the bell icon. Keep in mind that **CloudShell** is **a temporary environment**. All running processes will be **terminated once you close your CloudShell session or exit the AWS Console**.

## Install Python, Pip and Git on EC2 Instance

1. Check Python, Pip and Git versions. Execute per 1 line.
   ```bash
   python3 --version
   pip --version
   git --version
   ```

2. If an error occurs in number 1 then update the package list and install the missing package.
   ```bash
   sudo apt update -y

   # Install according to the error package
   sudo apt install python3 -y
   sudo apt install python3-pip -y
   sudo apt install git -y
   ```

3. Check the installed package version again as in number 1.

## Clone Source Code from GitHub

1. Clone GitHub repository.
   ```bash
   git clone https://github.com/syauqi-a/GetGrassMiner.git
   ```

2. Go to project folder.
  ```bash
  cd GetGrassMiner
  ```

## Create a Virtual Environment and Install Dependencies

It is recommended to still create **virtual environment**.

1. (**Optional**) If the `virtualenv` package does not exist, install it first:
   ```bash
   sudo pip3 install virtualenv
   ```

2. Create and activate **virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies from the `requirements.txt` file.
   ```bash
   pip install -r requirements.txt
   ```

## Setting up configuration

Make configuration settings in the `.env`, `config.json` and `proxies.txt` files as when running locally, see [here](README.md#setting-up-env-file).

## Running a Python Bot

Run the main script to start the bot.
```bash
python main.py
```

## Tips: Keeping the Bot Running

If you want the application to **keep running** even if you exit SSH, use the following method:
```bash
nohup python main.py > /dev/null 2>&1 & echo $! > nohup_main.pid
```

**Note**:

- By adding `> /dev/null 2>&1` all standard output (`stdout`) and error output (`stderr`) will not be saved to prevent storage bloat.

- See `main.py` process running in the background.
  ```bash
  ps -ef | grep main.py
  ```

- See the process in more detail.
  ```bash
  htop
  ```
  Then press F4, enter `main.py` and press ENTER. To exit press Q.

- Terminates the `main.py` process running in the background.
  ```bash
  kill $(cat nohup_main.pid)
  ```
