from itertools import chain
from operator import attrgetter

from projects.models.project import TranslationProject
from skills.models import TranslationSkill, LanguageSet


def get_suggested_projects(user):
    translation_projects = TranslationProject.objects.none()
    translation_skill = TranslationSkill.objects.filter(user=user)[0]
    language_sets = LanguageSet.objects.filter(translation_skill=translation_skill)
    for language_set in language_sets:
        tmp_translation_projects = TranslationProject.objects.filter(from_language=language_set.from_language,
                                                                     to_language=language_set.to_language,
                                                                     is_verified=True,
                                                                     is_started=False,
                                                                     ).exclude(client=user)
        translation_projects = translation_projects | tmp_translation_projects

    result_list = sorted(
        chain(translation_projects[:10]),
        key=attrgetter('release_date'))

    return result_list
    #suggested_projects = Project.objects.filter()