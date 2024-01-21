# User-Behavior-Based-Authentication-System
Creating a secure User Behavior-Based Authentication System using unique typing patterns instead of passwords. Captures key press details to form distinct user profiles, analyzed by an AI model. Retraining mechanism adapts to changing habits. Anomalies trigger discreet user notifications, enhancing security and user-friendliness.

### Problem Statement and Background  
User authentication is a critical aspect of modern digital security systems. Traditional methods like passwords have limitations, including susceptibility to theft, loss, or weak choices by users. Traditional methods of user authentication, such as passwords and biometrics, are susceptible to security breaches and user inconvenience. The aim of this project is to address these shortcomings by developing an innovative User Behavior-Based Authentication System that leverages unique typing patterns and habits for enhanced security and user authentication.

The core concept of our system is to develop a keylogger that secretly captures and analyzes the user's typing behavior, focusing on features such as keypress duration and time intervals between keypresses. This behavioral data is then used to create a distinctive user profile, effectively replacing, or supplementing traditional authentication methods.
To make this system effective, we will employ artificial intelligence (AI) techniques to design and train a model capable of analyzing the collected user behavior data. The AI model will continuously assess whether the current typing behavior matches the established patterns for the authorized user. This will provide a dynamic way to authenticate the users.
One of the key challenges to address is the need for a retraining mechanism to adapt to the user's changing typing habits over time. This mechanism ensures that the system remains accurate and up to date with the evolving trends of the user, maintaining a high level of security while minimizing false positives.
In the event of an anomaly or suspicious behavior, predefined options for handling it will be provided to the user, including discreet notifications or the option to force shutdown the computer. This user-friendly approach ensures that the user is informed and retains control over their system's security.

### Scope and Depth  
The following are the goals and objectives that this project will aspire to achieve.
The Functional Goals:
•	Collect data on keypress durations and time intervals between keypresses.
•	Analyze this data to create a user-specific typing profile.
•	Design and train an AI model capable of recognizing and distinguishing individual user patterns.
•	Continuously retrain and fine-tune the model to adapt to evolving typing habits.
•	Use the AI model to assess whether the current typing behavior matches the established user patterns.
•	Allow authorized users to access the system based on successful authentication.
•	Provide predefined options for handling anomalies, such as discreet notifications or system shutdown.
•	Ensure that the system remains non-intrusive and transparent to the user.
•	Design the system to handle data from a single user but with the potential for future scalability to accommodate multiple users.
The Non-Functional Goals:
•	Ensure the collected user behavior data remains secure and cannot be accessed or tampered with by unauthorized parties.
•	Achieve a high level of accuracy in recognizing and distinguishing user patterns to minimize false positives.
•	Create a robust and reliable system that functions without bugs or errors.
•	Make the source code accessible to the public to encourage transparency and collaboration.
The following are the goals and objectives that this project will not aim to achieve:
The Functional Goals:
•	User registration, account recovery, and account management functionalities are outside the scope of your project. This project focuses on the authentication aspect rather than the broader user management process.
•	This project is primarily designed for a single user's computer. Handling multiple user profiles and access control for shared devices would be a separate project scope.
The Non-Functional Goals:
•	Protecting against network-based attacks and unauthorized access over a network is beyond the scope of your project. Your project is primarily focused on physical access through the keyboard.
•	Ensuring that the system complies with legal regulations, such as data privacy laws like GDPR or HIPAA.
•	While this project will be developed for a specific platform, ensuring cross-platform compatibility (e.g., Windows, macOS, Linux) is an additional non-functional goal is out of scope.
•	Providing real-time feedback to users on their typing behavior, such as notifications and alerts, is a complex real-time feature and will be out of scope.

### Methodology  
Software Development Methodology: We will follow an iterative and adaptive software development methodology, combining elements of Agile and Iterative Development. This approach allows for flexibility and continuous improvement throughout the project's development stages. We will regularly review and refine the system based on feedback and emerging requirements.
Algorithms: The core of our project relies on machine learning algorithms to recognize and distinguish user patterns. Two key algorithms we plan to use are:
k-Nearest Neighbors (KNN): KNN is a non-parametric, supervised learning classifier that uses proximity to make classifications or predictions about the grouping of an individual data point. We intend to use KNN to build the initial AI model for user behavior recognition.
Support Vector Machines (SVM): SVM is another powerful algorithm for classification and regression analysis. We will explore the potential of SVM to enhance the accuracy and robustness of our AI model.
These algorithms will be implemented and fine-tuned to create a reliable and adaptable system for user authentication based on behavior patterns. Their effectiveness will be evaluated during the testing phase outlined in the Test Plan section.

### Innovation  
By using the inherent distinctiveness of individual typing behaviors, our project introduces a ground-breaking method of user authentication. Our User Behavior-Based Authentication System pioneers the use of sophisticated keylogging techniques to record and analyze personalized typing patterns rather than relying on traditional methods like passwordsor biometrics. This innovation not only significantly improves security but also promotes a more user-friendly environment.
We are pushing the limits of authentication technology by providing secret anomaly handling options and using artificial intelligence to continuously adapt to the user's changing typing habits. This opens the possibility of a future where convenience and security coexist peacefully.

### Complexity  
Our User Behavior-Based Authentication System is a complex and multi-application process. We seamlessly integrate keylogging capabilities into the user's computing environment while ensuring absolute privacy and data security. 
Data Capture - We capture and analyze a wide array of typing behavior attributes, including keypress durations and intervals, using a sophisticated data collection mechanism. 
Training Model - We design and train the AI model to recognize and distinguish individual user patterns from this data, requiring expertise in machine learning and artificial intelligence. We continuously retrain and fine-tune the model to adapt to the evolving typing habits of users over time.
We ensure that the system remains non-intrusive and transparent to the user while offering meaningful and secure feedback in the event of anomalies. Our approach is innovative and sophisticated, highlighting the depth and complexity of our User Behavior-Based Authentication System.

### Technical Challenges  
We have never taken on a project of this magnitude entirely on our own before. We are excited to work with AI outside of the classroom for a personal project. Creating a keylogger represents a novel and captivating challenge in my journey. The task of seamlessly integrating all the components and making these parts work without any hiccups with one another will be very challenging and hopefully fulfilling in the end. 
Gathering of data and training the model: Since our program aims to secure the computer of a single user, we only need the typed data of that individual. If a person types a 100-word paragraph, then that gives us 100 data points to train our model on. 
On paper, we feel that a k-nearest neighbor model (KNN), which is a non-parametric, supervised learning classifier, which uses proximity to make classifications or predictions about the grouping of an individual data point, will give us the best result. Testing and training multiple different models will be the best way to determine which model will be the best. Other model which will give us the best result could be Support Vector Machines (SVM).


