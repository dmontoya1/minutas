from tratum.store.models import UserSubscription, UserDocumentsSubscription


def context_subscription(request):
    try:
        user_subscription = UserSubscription.objects.filter(user=request.user).first()
        document_count = UserDocumentsSubscription.objects.filter(
            user_subscription=user_subscription,
            user_document__user=request.user
        ).count()
        can_add_document = False
        print("Documentos de la suscription", user_subscription.subscription.document_number)
        print("Documentos del user", document_count)
        if user_subscription.subscription.document_number < document_count:
            can_add_document = True
        print(can_add_document)
        return {
            'user_subscription': user_subscription,
            'user_subscription_count': document_count,
            'can_add_document': can_add_document
        }
    except:
        print("EXCEPT")
        return {
            'user_subscription': None,
            'user_subscription_count': 0,
            'can_add_document': False
        }
