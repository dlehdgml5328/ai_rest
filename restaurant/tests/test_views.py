from django.test import TestCase


class IndexViewTest(TestCase):
    def test_index_view(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        # assertTemplateUsed 메서드
        # 뷰(view)가 특정 템플릿을 사용하여 응답을 생성했는지를 검증하는 데 사용
        self.assertTemplateUsed(response, "index.html")
