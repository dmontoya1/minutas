from django.db import models
from django.core.exceptions import ValidationError


class Policy(models.Model):
    """Guarda las políticas de la plataforma

    Campos del modelo:
        content: Contenido de la política
        last_update_date: Indica cuando se realizó la última actualización del registro
        police_type: Tipo de política, sólo puede existir un registro por tipo

    """

    TERMS_AND_CONDITIONS = 'TCP'
    PRIVACY = 'PP'
    COOKIES_MANAGEMENT = 'CMP'

    POLICY_TYPE = (
        (TERMS_AND_CONDITIONS, 'Términos y condiciones'),
        (PRIVACY, 'Política de privacidad y tratamiento de datos'),
        (COOKIES_MANAGEMENT, 'Política de tratamiento de Cookies'),
    )

    content = models.TextField('Contenido')
    last_update_date = models.DateTimeField(
        'Fecha de última actualización',
        auto_now_add=True
    )
    policy_type = models.CharField(
        "Tipo de Política",
        max_length=3,
        choices=POLICY_TYPE,
        unique=True
    )

    def __str__(self):
        return "%s" % (self.policy_type)

    class Meta:
        verbose_name = "Politica"


class FAQCategory(models.Model):
    """Guarda las categorías de las preguntas frecuentes

    Campos del modelo:
        name: Nombre de la categoría

    """

    name = models.CharField(
		'Nombre',
        max_length=30,
        unique=True
    )

    class Meta:
        verbose_name = 'FAQ'

    def __str__(self):
        return self.name


class FAQItem(models.Model):
    """Guardas las preguntas frecuentes, por categoria

    Campos del modelo:
        category: Llave foránea nula a categoría
        question: Texto de la pregunta
        answer: Texto de la respuesta

    """

    category = models.ForeignKey(
        FAQCategory,
        models.SET_NULL,
        null=True,
        blank=True
    )
    question = models.TextField('Pregunta', unique=True)
    answer = models.TextField('Respuesta', unique=True)

    class Meta:
        verbose_name = 'Item de categoria'
        verbose_name_plural = 'Items de categoria'

    def __str__(self):
        return self.question


class SiteConfig(models.Model):
    """Guarda la información del sitio estático (Landing page y quienes sómos)

    Campos del modelo:
        about_page_title: Nombre de la página de Quienes sómos
        about_page_content: Contenido de la página de Quienes sómos
        about_page_image: Imagen de la página de Quienes sómos

    """

    about_page_title = models.CharField(
		'Título (Quienes sómos)',
        max_length=30,
        null=True,
        blank=True
    )
    about_page_content = models.TextField(
		'Contenido (Quienes sómos)',
        max_length=600,
        null=True,
        blank=True
    )
    about_page_image = models.ImageField(
        'Imagen (Quienes somos)',
        null=True,
        blank=True,
        upload_to='about-us',
        help_text='La resolución requerida es de 800x1000px'
    )
    landing_contact = models.TextField(
        'Correo de contacto (landing)',
        null=True,
        blank=True
    )
    landing_phone = models.TextField(
		'Teléfono de contacto (landing)',
        null=True,
        blank=True
    )
    landing_contract_info = models.TextField(
		'¿Por qué construir un contrato responsablemente? (landing)',
        null=True,
        blank=True
    )
    facebook_url = models.URLField(
		'URL Facebook (landing)',
        null=True,
        blank=True
    )
    twitter_url = models.URLField(
		'URL Twitter (landing)',
        null=True,
        blank=True
    )
    instagram_url = models.URLField(
		'URL Instagram (landing)',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Configuración de sitio'
        verbose_name_plural = verbose_name

    def __str__(self):
        return 'Registro de configuración de sitio'
    
    def clean(self):
        """Retorna ValidationError si se intenta crear más de una instancia
        """

        model = self.__class__
        if (model.objects.count() > 0 and
                self.id != model.objects.get().id):
            raise ValidationError(
                "Sólo se puede crear una instancia de %s." % model.__name__)


class SliderItem(models.Model):
    image = models.ImageField('Imagen', upload_to='slides')
    text = models.CharField(
        'Texto',
        max_length=255,
        null=True,
        blank=True
    )
    description = models.CharField(
        'Descripción',
        max_length=255,
        null=True,
        blank=True
    )
    youtube_video_link = models.URLField(
        'Link de Youtube',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Slide del home'
        verbose_name_plural = 'Slides del home'

    def __str__(self):
        return 'Slide '

