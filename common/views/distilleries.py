from django.shortcuts import render_to_response


def distilleries(request):
    context = {'page': 'distilleries',
               'distilleries': []}

    for still_id in range(1, 6):
        still = {
            'name': 'Distillery #%s' % still_id,
            'id': still_id}
        context['distilleries'].append(still)

    return render_to_response('distillery/distilleries.html', context)

