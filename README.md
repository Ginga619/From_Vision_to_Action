# From_Vision_to_Action
# Gesture-Based Math Solver Application  

A Python-based interactive application for drawing mathematical expressions using hand gestures, solving them with AI, and providing real-time feedback.  

## Features  
- **Gesture Control**:  
  - Draw expressions with your index finger.  
  - Erase using thumb and index finger.  
  - Clear the canvas with thumb and pinky.  
  - Submit expressions to AI using a specific gesture.  
- **AI-Powered Solutions**: Get math problems solved with the Google Generative AI model.  
- **Real-Time Interaction**: Uses a webcam for hand tracking and a dynamic canvas for drawing.  
- **Audio Feedback**: Confirms actions through sound.  

## Technologies Used  
- **Libraries**:  
  - [Streamlit](https://streamlit.io/) for the web interface.  
  - [OpenCV](https://opencv.org/) and [cvzone](https://github.com/cvzone) for hand gesture detection.  
  - [Google Generative AI](https://cloud.google.com/generative-ai) for solving math problems.  
  - [Pygame](https://www.pygame.org/) for audio feedback.  
  - [Pillow](https://python-pillow.org/) for image processing.  
- **Tools**: Python, dotenv for environment variables.  

## Installation  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/your-username/gesture-math-solver.git  
   cd gesture-math-solver  
   ```  

2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. Set up environment variables:  
   - Create a `.env` file in the project root.  
   - Add your Google API key:  
     ```  
     google_api=YOUR_API_KEY  
     ```  

4. Run the application:  
   ```bash  
   streamlit run app.py  
   ```  

## How to Use  

1. Allow webcam access when prompted.  
2. Follow the gesture guide:  
   - **Draw**: Use your index finger to draw expressions.  
   - **Erase**: Thumb + Index finger.  
   - **Clear Canvas**: Thumb + Pinky.  
   - **Submit**: All fingers except the ring finger.  
3. View AI solutions on the screen and hear feedback sounds.  


## Future Improvements  
- Add more gestures for advanced controls.  
- Support for complex equations and graph plotting.  
- Improve the UI for better user experience.  

## Contributing  
Contributions are welcome! Open an issue or submit a pull request to suggest features or fix bugs.  

## License  
This project is licensed under the [MIT License](LICENSE).  

## Acknowledgments  
- Thanks to [cvzone](https://github.com/cvzone) for hand gesture tracking modules.  
- Google Generative AI for problem-solving capabilities.  

---  

Feel free to let me know if any changes are needed!
