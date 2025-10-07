from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import SubmissionForm
from .models import Submission

def submit_view(request):
    if request.method == "POST":
        form = SubmissionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you — your submission has been recorded.")
            return redirect("submit")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = SubmissionForm()
    return render(request, "submission.html", {"form": form})

def submissions_list(request):
    data = Submission.objects.all().order_by("-created_at")
    return render(request, "list.html", {"submissions": data})

