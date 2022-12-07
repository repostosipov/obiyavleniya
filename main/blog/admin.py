from django.contrib import admin

from .models import Post, Category, Comment, PostImage, Help


class PostImageAdmin(admin.StackedInline):
    model=PostImage

class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "category",
        "created_ad",
        "updated_ad",
        "is_published",
    )
    list_display_links = ("id", "title")
    search_fields = ("title", "content")
    list_editable = ("is_published",)
    list_filter = ("is_published", "category")
    inlines = [PostImageAdmin]

    class Meta:
        model=Post


class PostImageAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    list_display_links = ("id", "title")
    search_fields = ("title",)

    class Meta:
        verbose_name = "Категорию"


admin.site.register(Post, PostAdmin)
admin.site.register(Category)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'body')
admin.site.register(Comment, CommentAdmin)

class HelpAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    list_filter = ('created')
    search_fields = ('name', 'body')


admin.site.register(Help)
