# Bank-Management-System


Project Overview

The Bank Account Management System is a menu-driven desktop application built using Python with the Tkinter GUI library.
It allows users to log in securely, perform banking operations (deposit, withdraw, check balance), and log out, all through a simple and interactive graphical interface.

This project simulates the working of a real-world banking portal in a simplified student-friendly format, focusing on the concepts of object-oriented programming (OOP), event-driven GUI programming, and user authentication.

Key Features
🔐 Login & Logout System

Users must log in with valid credentials before accessing account features.

Logout option ensures proper session handling and returns the user to the login screen.

📋 Menu-Driven Interface

After login, users are presented with a clear menu screen with buttons for different actions.

Easy navigation between screens ensures a smooth user experience.

💰 Banking Operations

Deposit Money – Add funds to the account with input validation.

Withdraw Money – Withdraw funds with balance checks to prevent overdrawing.

Check Balance – Instantly view the current balance.

Exit Application – Close the program safely.

🖥 Graphical User Interface (GUI)

Built using Tkinter for a clean and interactive design.

Provides buttons, labels, entry boxes, and message popups for real-time interaction.

Technology Stack

Programming Language: Python

GUI Library: Tkinter

Concepts Used:

Object-Oriented Programming (classes for BankAccount & GUI management)

Event-driven programming (button clicks trigger actions)

Exception handling and validation (invalid inputs, insufficient balance)

Workflow / How it Works

Launch the Application – The Tkinter window opens at the login page.

Login – The user enters valid credentials (username/password).

Menu Screen – On successful login, the user sees a menu with options:

Deposit

Withdraw

Check Balance

Logout / Exit

Perform Operations – Users can deposit, withdraw, or check balance interactively.

Logout – User logs out and is redirected back to the login page.
