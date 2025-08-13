
import csv

def convert_json_to_csv(data):
    try:
        csv_file = 'final_report.csv'
            # Specify the column headers
        fieldnames = ['question', 'answer', 'score', 'feedback']

        # Writing data to CSV
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        return True
    except Exception as e:
        print('➡ Error in convert json to csv:', e)
        raise e
        return False

# interview_report_dummy = [
#         {
#             "question": "Can you describe in detail the technology stack and the architecture of the 'Chat with Database' project that you worked on at Dhyey Consulting Gujarat?",
#             "answer": "hello hello"
#         },
#         {
#             "question": "You have mentioned the use of Docker for containerization in your previous roles. Can you discuss what specific problems this technology helped you solve and how it enabled seamless deployment across environments?",
#             "answer": "yeah I used docker containerization in the my previous role and I get many projects a problems"
#         },
#         {
#             "question": "In your AI/ML intern role at Techxi Gujarat, you mentioned that you led the development of machine learning projects, resulting in a 30 percent improvement in operational efficiency. Can you talk more about these projects and how you achieved this improvement?",
#             "answer": "yeah I used docker containerization in the my previous role and I get many projects a problems"
#         },
#         {
#             "question": "You listed AWS in your technical skills. Can you provide an example of a use case from your professional experience where you have used AWS in an AI/ML project?",
#             "answer": "yeah I used docker containerization in the my previous role and I get many projects a problems"
#         },
#         {
#             "question": "You have worked on ML applications such as PDF ChatBots, website URL ChatBots, resume converters and image generation tools. Can you highlight how you used AI/ML to develop these applications at Techxi Gujarat?",
#             "answer": "yeah I used docker containerization in the my previous role and I get many projects a problems"
#         }
#     ]

