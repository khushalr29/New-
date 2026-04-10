from django.db import models
from ..core.base import TenantModel

class MediaFolder(TenantModel):
    name = models.CharField(max_length=255)
    
    class Meta:
        db_table = 'media_folder'
        verbose_name = 'Media Folder'
        verbose_name_plural = 'Media Folders'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.company.company_name if self.company else 'Global'})"

class UploadMedia(TenantModel):
    file = models.TextField(null=True, blank=True)
    file_name = models.CharField(max_length=255)
    file_size = models.BigIntegerField(help_text="Size in bytes", null=True, blank=True)
    file_type = models.CharField(max_length=100, help_text="MIME type (e.g. image/png)", null=True, blank=True)
    extension = models.CharField(max_length=10, null=True, blank=True)
    folder = models.ForeignKey(MediaFolder, on_delete=models.CASCADE, null=True, blank=True, related_name='media_files')

    class Meta:
        db_table = 'upload_media'
        verbose_name = 'Upload Media'
        verbose_name_plural = 'Upload Media'
        ordering = ['-created_at']

    def __str__(self):
        return self.file_name or (self.file.name if self.file else "Unnamed File")