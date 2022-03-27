import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question

class QuestionModelTest(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="Who is the best platzi's CD ?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
        
    def test_was_published_recently_with_past_questions(self):
        """was_published_recently returns False for questions whose pub_date is in the past"""
        time = timezone.now() - datetime.timedelta(days=15)
        past_question = Question(question_text="Who is the best platzi's CD ?", pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)
        
        
    def test_was_published_recently_with_recent_questions(self):
        """was_published_recently returns True for questions whose pub_date is recently"""
        time = timezone.now()
        recent_question = Question(question_text="Who is the best platzi's CD ?", pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):
        """
        Create a question with the given question text, and published the given 
        number of day offset to now (negative for question published in the past,
        positive for questions that have yet to be published)
        """
        time = timezone.now() + datetime.timedelta(days=days)
        return Question.objects.create(question_text=question_text, pub_date=time)       
    
class QuestionIndexViewTest(TestCase):
    
    def test_no_question(self):
        """If no question, exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_future_question_no_published(self):
        """If question pub date is in the future, don't show it in the index page"""
        response = self.client.get(reverse("polls:index"))
        time = timezone.now() + datetime.timedelta(days=15)
        future_question = Question(question_text="Who is the best Platzi's Course Director ?", pub_date=time)
        self.assertNotContains(response, future_question)
      
    
    def test_future_question(self):
        """
        Question with a pub_date in the future aren't displayed  on the index page.
        """
        create_question("future_question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_past_question(self):
        """
        Question with a pub_date in the future aren displayed on the index page.
        """
        question=create_question("past_question", -10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
    
    
    def test_future_question_and_past_question(self):
        """
        Even if both past and future question exist, only past question are displayed
        """
        past_question = create_question("past question", -30)
        future_question = create_question("future question", 30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question]
        )
    

    def test_two_past_questions(self):
        """
        The question index page may display multiple questions.
        """
        past_question1 = create_question("past question 1", -10)
        past_question2 = create_question("past question 2", -19)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            [past_question1, past_question2]
        )
        
        
    def test_two_future_questions(self):
        """
        The question index page can't display multiple questions.
        """
        future_question1 = create_question("future question 1", 10)
        future_question2 = create_question("future question 2", 19)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            []
        )


class QuestionDetailViewTest(TestCase):
    
    def test_future_question(self):
        """
        The datail view of a question with a pub_date in the future
        returns a 404 error no found
        """
        future_question = create_question("future question", 10)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """
        The datail view of a question with a pub_date in the past
        displays the question's text
        """
        past_question = create_question("past question", -10)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
        
class ResultsViewTest(TestCase):
    pass