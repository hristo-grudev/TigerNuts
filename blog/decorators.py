from django.shortcuts import redirect


def group_required(groups=[]):
	group_set = set(groups)

	def decorator(view_func):
		def wrapper(request, *args, **kwargs):
			if request.user.is_superuser:
				return view_func(request, *args, **kwargs)
			# raw_groups = request.user.groups.only('name')
			raw_groups = request.user.groups.all()
			user_groups = set([group.name for group in raw_groups])
			print(user_groups)
			if user_groups.intersection(group_set):
				return view_func(request, *args, **kwargs)
			else:
				return redirect('view home')
		return wrapper
	return decorator
