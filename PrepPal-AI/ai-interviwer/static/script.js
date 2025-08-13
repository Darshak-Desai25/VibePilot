document.getElementById("submitformid").addEventListener('click', async function () {
    console.log('Interview Started...');

    const name = document.getElementById("name_id").value;
    const jobRole = document.getElementById("job_role_id").value;
    const resumeFile = document.getElementById("resume_id").files[0];

    const formData = new FormData();
    formData.append("uploaded_resume", resumeFile);
    formData.append("name", name);
    formData.append("job_role", jobRole);

    try {
        const response = await fetch('/start_interview', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();

        if (data.status === 'success') {
            console.log('Interview setup complete');
            document.getElementById('submit_details_id').style.display = 'none';
            document.getElementById('header_id').innerHTML = 'Interview Started';
            document.getElementById('submit_answer_id').style.display = 'block';
            document.getElementById('answer_display_id').style.display = 'none'; // Hide answer display initially

            // Display the first question
            displayQuestion(data.current_question, data.question_index);
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

// Function to display the current question and start Text-to-Speech
function displayQuestion(currentQuestion, index) {
    document.getElementById('question_id').innerHTML = currentQuestion;
    document.getElementById('question_index_id').innerHTML = index + 1; // Displaying the question index (1-based)
    document.getElementById('answer_text_id').innerText = ''; // Clear previous answer text
    document.getElementById('answer_display_id').style.display = 'none'; // Hide answer display
    speakText(currentQuestion); // Start speaking the question
}

// Text-to-speech conversion for questions
function speakText(que_data) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(que_data);
        utterance.onend = function () {
            console.log('Speech finished, starting STT...');
            startSTT();  // Start Speech-to-Text after TTS ends
        };
        speechSynthesis.speak(utterance);
    } else {
        alert('Sorry, your browser does not support text-to-speech.');
    }
}

// Function to start Speech-to-Text (STT)
let recognition;

function startSTT() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;  // Not keeping recognition active continuously
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.start();

        recognition.onstart = function () {
            console.log('Voice recognition started. You can speak now.');
        };

        recognition.onresult = function (event) {
            let transcript = '';
            for (let i = 0; i < event.results.length; i++) {
                transcript += event.results[i][0].transcript;
            }
            document.getElementById('answer_text_id').innerText = transcript;
            document.getElementById('answer_display_id').style.display = 'block'; // Show answer display
        };

        recognition.onerror = function (event) {
            console.error('Error occurred in recognition:', event.error);
        };
    } else {
        alert('Sorry, your browser does not support speech recognition.');
    }
}

// Stop recording when "Complete Answer" button is clicked
document.getElementById('submit_answer_id').addEventListener('click', async function () {
    if (recognition) {
        recognition.stop();  // Stop the recognition service only when the button is clicked
        console.log('STT stopped manually by the user.');

        const answer_data = document.getElementById("answer_text_id").innerText;
        let question = document.getElementById("question_id").innerText;

        const formData = new FormData();
        formData.append("answer_data", answer_data);
        formData.append("question", question);

        try {
            const response = await fetch('/record_answer', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            if (data.status === 'success') {
                console.log('Answer recorded.');
                document.getElementById('answer_text_id').innerText = ''; // Clear answer text for the next question
                proceedToNextQuestion();
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
});

// Function to proceed to the next question
async function proceedToNextQuestion() {
    const currentIndex = parseInt(document.getElementById('question_index_id').innerHTML) - 1; // Get current index (0-based)

    const response = await fetch(`/next_question/${currentIndex + 1}`); // Fetch next question using the next index
    const data = await response.json();

    if (data.status === 'success') {
        displayQuestion(data.current_question, data.question_index); // Display next question
    } else if (data.status === 'completed') {
        document.getElementById('question_id').innerHTML = "Interview completed. Thank you!";
        document.getElementById('generate_report_id').style.display = "block";
        document.getElementById('submit_answer_id').style.display = 'none'; // Hide the complete answer button
        document.getElementById('header_id').style.display = 'none';

        // Hide the answer display section after completing all questions
        document.getElementById('answer_display_id').style.display = 'none'; // Hide the answer display
    }
}

// Event listener for generating the report
document.getElementById('generate_report_id').addEventListener('click', async function () {
    // Hide the generate report button and show the loader
    document.getElementById('generate_report_id').style.display = 'none';
    document.getElementById('loader').style.display = 'block'; // Show the loader

    try {
        const response = await fetch('/generate_report', {
            method: 'GET'
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        if (data.status === 'success') {
            console.log(data.feedback);
            // You may want to trigger the download here as well, or provide a separate download button
            document.getElementById('download_report_id').style.display = 'block';  // Show the download button
        }
    } catch (error) {
        console.error('Error:', error);
    } finally {
        document.getElementById('loader').style.display = 'none'; // Hide the loader after report generation
    }
});

// Event listener for the download report button
document.getElementById('download_report_id').addEventListener('click', function () {
    window.location.href = '/download_report';  // Redirect to the download report endpoint
});
