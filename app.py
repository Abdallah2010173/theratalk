from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import re
import logging

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


response_dict = {
    
    'stress': [
        "It sounds like you're feeling stressed. Here are a few tips: try deep breathing exercises, take regular breaks, and consider speaking to a mental health professional.",
        "Stress can be overwhelming. Have you tried mindfulness or relaxation techniques? Sometimes talking things out can also help.",
        "I encourage you to spend time doing activities you love or exploring new hobbies as a form of relaxation.",
        "It's important to prioritize self-care and seek support when needed. Stress management can greatly benefit from professional help."
    ],
    'anxiety': [
        "Anxiety can be tough. Practicing mindfulness and staying active might help. If it becomes overwhelming, talking to a therapist could be useful.",
        "Feeling anxious is challenging. Have you tried keeping a journal or practicing relaxation techniques? These can sometimes help manage anxiety.",
        "Consider trying deep breathing exercises or engaging in physical activities to alleviate anxiety.",
        "Connecting with friends or a support group can also be beneficial in managing feelings of anxiety."
    ],
    'depression': [
        "If you're feeling depressed, reaching out to a mental health professional can provide you with support and treatment options.",
        "Depression can be difficult to handle alone. Talking to a counselor or therapist might offer the help and guidance you need.",
        "Maintaining a regular routine and seeking support from loved ones can be helpful when dealing with depression.",
        "It's important to acknowledge your feelings and seek help from a mental health professional if needed."
    ],
    'pulling': [
        "If you're struggling with hair-pulling or similar behaviors, consider reaching out to a mental health professional for support and strategies.",
        "Managing hair-pulling involves understanding its triggers. Speaking with a counselor can provide you with strategies to manage and reduce this behavior.",
        "Implementing stress-relief techniques and identifying triggers can help in managing hair-pulling.",
        "A mental health professional can work with you to develop a personalized plan to address hair-pulling behaviors."
    ],
    'trauma': [
        "You're not alone, and it's okay to seek help. Healing from trauma is a gradual process.",
        "It's important to allow yourself time to heal and to seek support from professionals who can guide you through the process.",
        "Talking to a therapist can help you work through traumatic experiences and develop coping strategies.",
        "Remember, it's okay to reach out for help and take things one step at a time in your healing journey."
    ],
    'loneliness': [
        "Feeling lonely can be difficult. Connecting with others, whether through support groups or social activities, can help.",
        "Consider reaching out to friends, family, or joining a community group to combat feelings of loneliness.",
        "Engaging in activities that bring you joy and fulfillment can also help alleviate loneliness.",
        "It might be helpful to talk to a counselor who can provide strategies for managing loneliness and building connections."
    ],
    'guilt': [
        "Guilt can be overwhelming. It might be helpful to talk about your feelings with a therapist or counselor.",
        "Understanding the root of your guilt and working through it with a mental health professional can be beneficial.",
        "It's important to address feelings of guilt and find ways to forgive yourself and move forward.",
        "Consider journaling about your feelings and seeking support to help manage and understand your guilt."
    ],
    'grief': [
        "Grief is a natural response to loss, and it's important to allow yourself time to grieve and seek support.",
        "Talking to a grief counselor or joining a support group can provide comfort and guidance during this time.",
        "Remember that grieving is a personal process, and seeking professional help can aid in navigating your emotions.",
        "Allow yourself to feel and express your grief, and consider reaching out to others who can offer support."
    ],
    'anger': [
        "Managing anger can be challenging. Techniques like deep breathing, exercise, and talking to a therapist can help.",
        "It's important to identify the triggers for your anger and work on strategies to address them effectively.",
        "Consider engaging in anger management therapy to help understand and control your emotional responses.",
        "Talking to a counselor can provide you with tools to manage and express your anger in a healthy way."
    ],
    'confidence': [
        "Building confidence can involve setting small, achievable goals and celebrating your successes.",
        "Consider working with a coach or therapist to develop strategies for improving your self-esteem and confidence.",
        "Engaging in positive self-talk and challenging negative thoughts can also help boost your confidence.",
        "It's important to recognize your strengths and work on areas where you feel less confident with supportive guidance."
    ],
    'self-esteem': [
        "Improving self-esteem often involves recognizing and valuing your worth. Therapy can be a great resource for this.",
        "Consider engaging in activities that build your sense of accomplishment and self-worth.",
        "Practicing self-compassion and challenging negative self-beliefs can help enhance your self-esteem.",
        "Support from a mental health professional can provide you with strategies to boost your self-esteem."
    ],
    'relationship': [
        "Healthy relationships involve communication and mutual respect. Seeking relationship counseling can help address issues.",
        "Consider working on communication skills and setting boundaries to improve your relationships.",
        "If you're facing difficulties in your relationships, talking to a counselor can offer valuable insights and strategies.",
        "Building strong relationships often involves understanding each other’s needs and working together to address concerns."
    ],
    'work': [
        "Work-related stress can be managed by setting boundaries, seeking support, and taking regular breaks.",
        "Consider discussing any work-related issues with a supervisor or a career counselor for support and guidance.",
        "It's important to balance work with personal time and seek help if work stress is impacting your well-being.",
        "Developing time management skills and finding ways to reduce work-related stress can also be beneficial."
    ],
    'sleep': [
        "Improving sleep can involve creating a bedtime routine, managing stress, and ensuring a comfortable sleep environment.",
        "Consider practicing relaxation techniques before bed and limiting screen time to enhance sleep quality.",
        "If sleep issues persist, consulting with a healthcare provider or sleep specialist might be necessary.",
        "Establishing a regular sleep schedule and addressing any underlying stress or anxiety can improve sleep."
    ],
    'motivation': [
        "Finding motivation can involve setting clear goals, rewarding yourself for progress, and seeking inspiration.",
        "Consider breaking tasks into smaller steps and focusing on your achievements to stay motivated.",
        "Working with a coach or therapist can provide strategies for maintaining motivation and overcoming obstacles.",
        "It's important to identify what drives you and create an action plan to stay motivated and focused."
    ],
    'social': [
        "Building social connections can be supported by joining groups, attending events, and reaching out to others.",
        "Consider engaging in social activities that interest you and foster new connections with like-minded individuals.",
        "Developing social skills and practicing communication can also help enhance your social interactions.",
        "If social interactions are challenging, seeking support from a therapist can provide guidance and strategies."
    ],
    'resilience': [
        "Building resilience involves developing coping strategies, maintaining a positive outlook, and seeking support when needed.",
        "Consider working on stress management techniques and seeking guidance from a mental health professional.",
        "Resilience can be strengthened by focusing on problem-solving skills and learning from challenges.",
        "It's important to recognize your strengths and work on building a support system to enhance resilience."
    ],
    'forgiveness': [
        "Forgiveness often involves letting go of past grievances and working towards healing. Therapy can support this process.",
        "Consider exploring your feelings about forgiveness and working through them with a counselor.",
        "Forgiving yourself and others can be a challenging process, and seeking support can aid in this journey.",
        "It's important to understand that forgiveness is a personal choice and can contribute to emotional healing."
    ],
    'self-care': [
        "Self-care involves taking time for yourself and engaging in activities that promote well-being. Consider developing a self-care routine.",
        "Prioritizing self-care can include physical, emotional, and mental health practices that support your overall well-being.",
        "Consider exploring different self-care activities and finding what works best for you.",
        "Maintaining regular self-care practices can help reduce stress and improve your overall quality of life."
    ],
    'identity': [
        "Exploring and understanding your identity can involve self-reflection, personal growth, and seeking support from a therapist.",
        "Consider engaging in activities that help you connect with your values and interests.",
        "Understanding your identity is a personal journey, and seeking professional guidance can provide support.",
        "It's important to explore what makes you unique and find ways to embrace and express your true self."
    ],
    'boundaries': [
        "Setting healthy boundaries is important for maintaining well-being and managing relationships. Consider working with a counselor to establish boundaries.",
        "Developing clear and respectful boundaries can improve your interactions and reduce stress.",
        "It can be helpful to communicate your boundaries clearly and practice assertiveness.",
        "Seeking support in setting and maintaining boundaries can contribute to healthier relationships and personal growth."
    ],
    'addiction': [
        "If you're struggling with addiction, seeking professional help and support groups can be beneficial.",
        "Consider working with a counselor or therapist to develop strategies for overcoming addiction.",
        "Recovery from addiction often involves building a support network and addressing underlying issues.",
        "It's important to seek help and resources to support your journey towards recovery and well-being."
    ],
    'self-improvement': [
        "Self-improvement can involve setting personal goals, seeking feedback, and engaging in continuous learning.",
        "Consider identifying areas for growth and developing a plan to work on self-improvement.",
        "Working with a coach or therapist can provide guidance and support in your self-improvement journey.",
        "It's important to celebrate your progress and remain motivated in your pursuit of personal growth."
    ],
    'anger-management': [
        "Managing anger involves identifying triggers, practicing relaxation techniques, and seeking support if needed.",
        "Consider working on strategies for expressing and managing anger in a healthy way.",
        "Anger management can benefit from counseling and developing coping mechanisms.",
        "It's important to address and manage anger constructively to improve your overall well-being."
    ],
    'emotional-intelligence': [
        "Developing emotional intelligence involves understanding and managing your emotions, as well as empathizing with others.",
        "Consider working on skills such as self-awareness, empathy, and emotional regulation.",
        "Improving emotional intelligence can enhance your relationships and personal growth.",
        "Seeking guidance from a therapist or coach can support your development in emotional intelligence."
    ],
    'confidence': [
        "Building confidence involves setting achievable goals, recognizing your strengths, and challenging negative thoughts.",
        "Consider seeking feedback and engaging in activities that build your self-esteem.",
        "Working with a therapist or coach can help you develop strategies to boost your confidence.",
        "It's important to celebrate your successes and focus on positive self-talk to enhance confidence."
    ],
    'assertiveness': [
        "Being assertive involves expressing your needs and opinions clearly and respectfully.",
        "Consider practicing assertiveness skills and setting boundaries in your interactions.",
        "Working with a therapist can help you develop and maintain assertive communication skills.",
        "It's important to balance assertiveness with empathy and understanding in your relationships."
    ],
    'creativity': [
        "Fostering creativity involves exploring new ideas, experimenting with different approaches, and allowing yourself to be innovative.",
        "Consider engaging in creative activities and seeking inspiration from various sources.",
        "Working on creative projects can enhance your problem-solving skills and self-expression.",
        "It's important to nurture your creative interests and find ways to incorporate them into your daily life."
    ],
    'self-awareness': [
        "Developing self-awareness involves reflecting on your thoughts, feelings, and behaviors.",
        "Consider keeping a journal and seeking feedback from others to enhance your self-awareness.",
        "Working with a therapist can provide insights and support in understanding yourself better.",
        "It's important to regularly check in with yourself and be mindful of your emotional and mental state."
    ],
    'goal-setting': [
        "Setting clear and achievable goals can help you stay focused and motivated.",
        "Consider breaking down larger goals into smaller steps and tracking your progress.",
        "Working with a coach or mentor can provide guidance and support in setting and achieving your goals.",
        "It's important to regularly review and adjust your goals as needed to stay on track."
    ],
    'time-management': [
        "Effective time management involves prioritizing tasks, setting deadlines, and using tools to stay organized.",
        "Consider developing a schedule and utilizing time management techniques to improve productivity.",
        "Working on time management skills can help reduce stress and enhance your efficiency.",
        "It's important to balance work and personal time to maintain a healthy lifestyle."
    ],
    'financial-stress': [
        "Managing financial stress involves creating a budget, seeking financial advice, and addressing concerns proactively.",
        "Consider developing a plan to manage your finances and seeking support if needed.",
        "Working with a financial advisor can provide guidance and strategies for reducing financial stress.",
        "It's important to address financial issues and develop a plan to achieve financial stability."
    ],
    'family-dynamics': [
        "Understanding and improving family dynamics involves open communication and seeking support if needed.",
        "Consider working on family relationships and addressing any conflicts with a counselor or therapist.",
        "It's important to foster positive family interactions and address issues collaboratively.",
        "Working on family dynamics can contribute to a healthier and more supportive family environment."
    ],
    'parenting': [
        "Effective parenting involves understanding your child's needs, setting boundaries, and providing support.",
        "Consider seeking parenting advice and strategies from professionals or support groups.",
        "It's important to balance discipline with empathy and foster a positive relationship with your child.",
        "Working on parenting skills can enhance your relationship with your child and support their development."
    ],
    'life-transitions': [
        "Navigating life transitions involves adapting to change and seeking support if needed.",
        "Consider working with a therapist or counselor to manage transitions and develop coping strategies.",
        "It's important to give yourself time to adjust and seek support during significant life changes.",
        "Embracing change and seeking guidance can help you navigate transitions more effectively."
    ],
    'personal-growth': [
        "Personal growth involves setting goals, seeking new experiences, and reflecting on your progress.",
        "Consider exploring opportunities for self-improvement and engaging in activities that challenge you.",
        "Working on personal growth can enhance your overall well-being and self-understanding.",
        "It's important to set aside time for reflection and continuous learning to support your personal development."
    ],
    'self-doubt': [
        "Dealing with self-doubt involves recognizing your strengths and seeking support to challenge negative thoughts.",
        "Consider working with a therapist to address and overcome self-doubt and build self-confidence.",
        "It's important to acknowledge your achievements and focus on positive self-affirmation.",
        "Seeking feedback and support can help you manage and reduce self-doubt effectively."
    ],
    'communication': [
        "Effective communication involves expressing yourself clearly and listening actively.",
        "Consider working on communication skills and seeking feedback to improve your interactions.",
        "It's important to practice active listening and assertiveness in your conversations.",
        "Working with a coach or therapist can provide guidance on enhancing your communication skills."
    ],
    'emotional-support': [
        "Seeking emotional support involves reaching out to others and expressing your feelings.",
        "Consider talking to friends, family, or a mental health professional for support.",
        "It's important to build a support network and seek help when needed for emotional well-being.",
        "Engaging in supportive conversations and activities can enhance your emotional resilience."
    ],
    'relaxation': [
        "Practicing relaxation techniques can help manage stress and improve your overall well-being.",
        "Consider incorporating activities like meditation, deep breathing, or yoga into your routine.",
        "It's important to find relaxation methods that work for you and prioritize them regularly.",
        "Working on relaxation techniques can contribute to better mental and physical health."
    ],
    'emotional-regulation': [
        "Managing emotional regulation involves understanding and controlling your emotional responses.",
        "Consider working on techniques such as mindfulness and cognitive-behavioral strategies.",
        "It's important to develop healthy coping mechanisms and seek support if needed.",
        "Working with a therapist can provide valuable tools and support for emotional regulation."
    ],
    'social-anxiety': [
        "Social anxiety can be challenging. Consider working with a therapist to develop coping strategies.",
        "Practicing social skills and gradually exposing yourself to social situations can help manage social anxiety.",
        "It's important to seek support and work on techniques to reduce anxiety in social settings.",
        "Building confidence and addressing underlying fears can improve your experience with social anxiety."
    ],
    'boundary-setting': [
        "Setting boundaries involves clearly communicating your needs and limits in relationships.",
        "Consider working with a counselor to establish and maintain healthy boundaries.",
        "It's important to practice assertiveness and respect in setting boundaries.",
        "Developing clear boundaries can improve your relationships and overall well-being."
    ],
    'self-compassion': [
        "Practicing self-compassion involves treating yourself with kindness and understanding.",
        "Consider working on self-compassion techniques and seeking support if needed.",
        "It's important to acknowledge your struggles and offer yourself the same compassion you would offer others.",
        "Building self-compassion can enhance your emotional resilience and well-being."
    ],
    'coping-skills': [
        "Developing coping skills involves finding effective ways to manage stress and challenges.",
        "Consider working on strategies such as problem-solving, relaxation, and seeking support.",
        "It's important to identify and practice coping skills that work best for you.",
        "Working with a therapist can provide valuable tools and techniques for managing difficult situations."
    ],
    'sad': [
        "That's alright, sometimes life can be hard but we should be able to overcome these problems.",
        "Why, You can tell me, Go Ahead ..."
    ],
    'hi': [
        " Hello \n\n   how can I help you ?"
    ],


}

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '').lower()
    print(f"Received message: {user_message}")
    response = suggest_solution(user_message)
    return jsonify({'response': response})

def suggest_solution(user_message):
    for keyword in response_dict:
        if re.search(r'\b' + re.escape(keyword) + r'\b', user_message):
            return random.choice(response_dict[keyword])
    
    return "Sorry, I didn't understand that. Could you please provide more details?"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
