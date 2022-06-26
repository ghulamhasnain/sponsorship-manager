"""school URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url

from emailsender import views as emailsender_views
from accounts import views as accounts_views
from students import views as student_views

urlpatterns = [
    url(r'^$', emailsender_views.Home.as_view(), name='home'),
    url(r'^orphan/$', emailsender_views.Orphans.as_view(), name='orphans'),
    url(r'^orphan/(?P<admitnumber>.+)/edit$', emailsender_views.EditOrphan.as_view(), name='edit_orphan'),
    url(r'^orphan/(?P<admitnumber>.+)/download$', emailsender_views.DownloadProfileOrphan.as_view(), name='download_profile_orphan'),
    url(r'^orphan/delete_all$', emailsender_views.DeleteAllOrphans.as_view(), name='delete_all_orphans'),

    url(r'^info/$', emailsender_views.Info.as_view(), name='information'),
    url(r'^info/delete_all$', emailsender_views.DeleteAllInfo.as_view(), name='delete_all_info'),

    url(r'^campaign/$', emailsender_views.Campaigns.as_view(), name='campaigns'),
    url(r'^campaign/(?P<name>.+)/edit$', emailsender_views.EditCampaign.as_view(), name='edit_campaign'),
    url(r'^campaign/newsletter$', emailsender_views.CampaignNewsletter.as_view(), name='campaign_newsletter'),

    url(r'^sponsor/$', accounts_views.Sponsors.as_view(), name='sponsors'),
    url(r'^sponsor/(?P<username>.+)/edit$', accounts_views.EditSponsor.as_view(), name='edit_sponsor'),
    url(r'^sponsor/delete_all$', accounts_views.DeleteAllSponsors.as_view(), name='delete_all_sponsors'),

    url(r'^sponsor/email/content$', accounts_views.ContentEmailSponsor.as_view(), name='content_email_sponsors'),
    url(r'^sponsor/email$', accounts_views.EmailSponsor.as_view(), name='email_sponsors'),

    url(r'^student/(?P<admitnumber>.+)/view$', student_views.ViewStudent.as_view(), name='view_student'),
    url(r'^student/upload$', student_views.Upload.as_view(), name='upload2'),
    url(r'^student/update$', student_views.UpdateStudents.as_view(), name='update_students'),
    url(r'^student/all$', student_views.AllStudents.as_view(), name='all_students'),
    url(r'^student/batch/all$', student_views.BatchStudents.as_view(), name='batch_students'),

    url(r'^medical/all$', student_views.AllMedical.as_view(), name='all_medical'),
    
    url(r'^upload/$', accounts_views.Upload.as_view(), name='upload'),
    url(r'^test/$', accounts_views.Test.as_view(), name='test'),
    url(r'^admin/', admin.site.urls),
]
