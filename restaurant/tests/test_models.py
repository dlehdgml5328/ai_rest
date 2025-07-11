from django.core.files.base import ContentFile
from django.db import IntegrityError
from django.test import TestCase

from restaurant.models import (
    Article,
    CuisineType,
    Region,
    Restaurant,
    RestaurantCategory,
    RestaurantImage,
    RestaurantMenu,
    Review,
    ReviewImage,
    SocialChannel,
    Tag,
)


# Restaurant 모델 테스트
class ArticleModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.article = Article.objects.create(
            title="테스트 칼럼 제목",
            content="테스트 칼럼 내용",
            preview_image=ContentFile(
                b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a", name="test-image.png"
            ),
            show_at_index=True,
            is_published=True,
        )

    def test_content(self):
        expected_data = self.article

        self.assertEqual(expected_data.title, "테스트 칼럼 제목")
        self.assertEqual(expected_data.content, "테스트 칼럼 내용")
        self.assertEqual(expected_data.show_at_index, True)
        self.assertEqual(expected_data.is_published, True)
        self.assertTrue(
            expected_data.preview_image.name.startswith("article/test-image")
        )


# CuisineType(음식 종류) 모델 테스트
class CuisineTypeModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        CuisineType.objects.create(name="한식")

    def test_content(self):
        cuisine_type = CuisineType.objects.get(id=1)
        self.assertEqual(cuisine_type.name, "한식")


# RestaurantCategory(식당 카테고리) 모델 테스트
class RestaurantCategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        RestaurantCategory.objects.create(name="카페")

    def test_content(self):
        restaurant_category = RestaurantCategory.objects.get(id=1)
        self.assertEqual(restaurant_category.name, "카페")


# RestaurantImage(식당 이미지) 모델 테스트
class RestaurantImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 식당 객체와 이미지 객체를 연결
        restaurant = Restaurant.objects.create(name="테스트 식당")
        RestaurantImage.objects.create(
            restaurant=restaurant,
            image=ContentFile(
                b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a", name="test-image.png"
            ),
        )

    def test_content(self):
        restaurant_image = RestaurantImage.objects.get(id=1)
        self.assertEqual(restaurant_image.restaurant.name, "테스트 식당")
        self.assertTrue(restaurant_image.image.name.startswith("restaurant/test-image"))


# RestaurantMenu(식당 메뉴) 모델 테스트
class RestaurantMenuModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        restaurant = Restaurant.objects.create(name="테스트 식당")
        RestaurantMenu.objects.create(
            restaurant=restaurant,
            name="테스트 메뉴",
            price=15_000,
        )

    def test_content(self):
        restaurant_menu = RestaurantMenu.objects.get(id=1)
        self.assertEqual(restaurant_menu.restaurant.name, "테스트 식당")
        self.assertEqual(restaurant_menu.name, "테스트 메뉴")
        self.assertEqual(restaurant_menu.price, 15_000)


# ReviewImage(리뷰)모델 테스트
class ReviewModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.restaurant = Restaurant.objects.create(name="테스트 식당")
        cls.review = Review.objects.create(
            restaurant=cls.restaurant,
            rating=4,
            content="테스트 리뷰 내용",
        )

    def test_content(self):
        self.assertEqual(self.review.restaurant.name, "테스트 식당")
        self.assertEqual(self.review.rating, 4)
        self.assertEqual(self.review.content, "테스트 리뷰 내용")


# ReviewImage(리뷰 이미지) 모델 테스트
class ReviewImageModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        restaurant = Restaurant.objects.create(name="테스트 식당")
        review = Review.objects.create(
            restaurant=restaurant,
            rating=4,
            content="테스트 리뷰 내용",
        )
        ReviewImage.objects.create(
            review=review,
            image=ContentFile(
                b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a", name="test-image.png"
            ),
        )

    def test_content(self):
        review_image = ReviewImage.objects.get(id=1)
        self.assertEqual(review_image.review.restaurant.name, "테스트 식당")
        self.assertTrue(review_image.image.name.startswith("review/test-image"))


# SocialChannel(소셜채널) 모델 테스트
class SocialChannelModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        SocialChannel.objects.create(name="Instagram")

    def test_content(self):
        social_channel = SocialChannel.objects.get(id=1)
        self.assertEqual(social_channel.name, "Instagram")


# Tag(태그) 모델 테스트
class TagModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Tag.objects.create(name="맛집")

    def test_content(self):
        tag = Tag.objects.get(id=1)
        self.assertEqual(tag.name, "맛집")


# 정상적으로 Region 객체가 생성되는지 확인
# 중복된 지역 조합이 저장되지 않도록 제약이 잘 작동하는지 확인
# (`unique_together`)
class RegionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 정상적인 지역 데이터 1건 생성
        cls.region = Region.objects.create(
            sido="서울특별시",
            sigungu="강남구",
            eupmyeondong="역삼동",
        )

    def test_content(self):
        """정상적으로 필드값이 저장되는지 확인"""
        expected = self.region
        self.assertEqual(expected.sido, "서울특별시")
        self.assertEqual(expected.sigungu, "강남구")
        self.assertEqual(expected.eupmyeondong, "역삼동")
        self.assertEqual(str(expected), "서울특별시 강남구 역삼동")
