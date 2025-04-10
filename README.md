# School Management System

A comprehensive application for managing students, disciplines, and grades with both console and GUI interfaces, featuring robust undo/redo functionality and multiple storage options.

## Features
![image](https://github.com/user-attachments/assets/ce51620d-cde0-437d-b593-69cfc0ca16d6)
![image](https://github.com/user-attachments/assets/f0b24bc6-99e6-4e89-892d-56c7494637dc)


### Core Functionality
- **Student/Discipline Management**
  - Add/Remove/Update students and disciplines
  - List all entities
- **Grading System**
  - Assign grades to students at disciplines
  - Automatic grade cleanup when removing students/disciplines
- **Advanced Search**
  - Case-insensitive partial matching for names
  - ID-based lookup
- **Statistics**
  - Failing students (average <5)
  - Top-performing students
  - Discipline performance rankings
- **Undo/Redo**
  - Uses Command Design Pattern for efficient memory usage 
  - Full history tracking for all operations
  - Cascaded operations for complex actions

### Technical Features
- Multiple Storage Backends
  - In-memory repository
  - Text file persistence
  - Binary file storage
- Layered Architecture
  - Clean separation between UI, Service, and Repository layers
  - Custom exception handling
- Automated Data Generation
  - Random student names using Faker
  - Default discipline list

## Installation

### Requirements
- Python 3.9+
- Required packages:
  ```bash
  pip install faker texttable
#User can choose between Console based UI and Graphical Interface
