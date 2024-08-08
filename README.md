# Two-Way Communication with GUI

## Overview

This project demonstrates a two-way communication system between a client and server using Python. The client and server applications are equipped with graphical user interfaces (GUIs) built with **PyQt6**. 

A key feature of this project is its use of **multithreading** to handle messaging. This ensures that both the client and server can send and receive messages concurrently without any interruption, providing a seamless and responsive communication experience.

## Features

- **Client and Server Communication**: A client can send messages to the server and receive messages from the server.
- **GUI Interface**: Both client and server applications have a graphical user interface for user interaction.
- **Multithreading**: Ensures that both sending and receiving messages can happen concurrently without blocking.
- **Logging**: Messages are logged to files for later review.

![image](https://github.com/user-attachments/assets/abc4df89-bc71-4233-89cd-0fe3c7c066c4)

## Usage

1. **First Start the Server**

   Run the server script first to start the server and wait for incoming connections:

   ```bash
   python testing_server.py

1. **Start the Client**

   Once the server is running, start the client script to connect to the server and enable two-way communication:
   ```bash
   python testing_client.py

And you're ready to text!


## Requirements

- Python 3.6 or higher
- PyQt6
- (Optional) Any modern IDE or text editor for development

## Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/velidagi/Two-Way-Communication-with-GUI.git
