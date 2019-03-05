from django.shortcuts import render
from .models import comments
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .forms import CommentForm

# Create your views here.
def comment_thread(request, id):
    print(id)
    obj = get_object_or_404(comments,id=id)
    instance_data = {
		'content_type' : obj.content_type,
		'object_id'    : obj.object_id,
	}
    form = CommentForm(request.POST or None , initial=instance_data)
    if form.is_valid():
        c_type 		 = form.cleaned_data.get('content_type')
        obj_id 		 = form.cleaned_data.get('object_id')
        content_type = ContentType.objects.get(model=c_type)
        content_data = form.cleaned_data.get('content')
        parent_obj   = None
        try:
            parent_id = int(request.POST.get("parent_id"))
        except:
            parent_idv= None
        if parent_id:
            qs = comments.objects.filter(id=parent_id)
            if qs.exists():
                parent_obj = qs.first()
        new_comment , created = comments.objects.get_or_create(
        user = request.user,
        content_type = content_type,
        object_id = obj_id ,
        content = content_data,
        parent = parent_obj

        )
        return HttpResponseRedirect(new_comment.content_object.get_absolute_url())

    context = {'comment':obj ,
                'form': form ,
     }
    return render(request, "comment_thread.html", context)
