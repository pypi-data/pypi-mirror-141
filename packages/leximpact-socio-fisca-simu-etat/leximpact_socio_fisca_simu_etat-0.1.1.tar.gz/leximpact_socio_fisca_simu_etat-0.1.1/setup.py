# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['leximpact_socio_fisca_simu_etat']

package_data = \
{'': ['*']}

install_requires = \
['OpenFisca-France==113.0.3',
 'fastapi>=0.63.0,<0.64.0',
 'gunicorn>=20.1.0,<21.0.0',
 'openfisca-france-reforms==1.0.82',
 'pandas>=1.2.4,<2.0.0',
 'prometheus-fastapi-instrumentator>=5.7.1,<6.0.0',
 'python-decouple>=3.5,<4.0',
 'python-jose[cryptography]>=3.3.0,<4.0.0',
 'redis>=3.5.3,<4.0.0',
 'ruamel.yaml>=0.17.21,<0.18.0',
 'tables>=3.6.1',
 'toolz>=0.11.1',
 'uvicorn[standard]>=0.13.4,<0.14.0']

entry_points = \
{'console_scripts': ['api = '
                     'leximpact_socio_fisca_simu_etat_api.server:start_dev']}

setup_kwargs = {
    'name': 'leximpact-socio-fisca-simu-etat',
    'version': '0.1.1',
    'description': '_HTTP + WebSocket API for OpenFisca',
    'long_description': '# French State Budget Simulation API\n\n\n\n\n_HTTP API for OpenFisca_\n\nUsed by [LexImpact](https://leximpact.an.fr/), a simulator of the French tax-benefit system.\n\nMake use of [OpenFisca](https://openfisca.org/en/) a rules as code tax benefit system.\n\n\n## Install\n\n`pip install leximpact_socio_fisca_simu_etat`\n\n## How to use\n\nFill me in please! Don\'t forget code examples:\n\n```python\nfrom leximpact_socio_fisca_simu_etat.csg_simu import (\n    ReformeSocioFiscale,\n    compute_all_simulation,\n)\n\nreform = ReformeSocioFiscale(\n    base=2021,\n    amendement={\n        "prelevements_sociaux.contributions_sociales.csg.activite.imposable.taux": 0.068,\n    },\n    output_variables=["csg"],\n    quantile_nb=4,\n    quantile_compare_variables=["csg"],\n)\nresultat = compute_all_simulation(reform, annee_de_calcul="2021")\n```\n\n    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:41] reform.amendement : None\n    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:41] No cache for 5078a86c7201f132a44472774283e4a774e85b9bd94c88c9e756d3cb2021, compute it.\n    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:45] OpenFisca a retourné des individus\n    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:45] reform.amendement : {\'prelevements_sociaux.contributions_sociales.csg.activite.imposable.taux\': 0.068}\n    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:45] No cache for 3580f21542881d1996a7b3a16a759d8318e58bdc44ac26ab6cfbf8662021, compute it.\n    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:49] OpenFisca a retourné des individus\n    [leximpact_socio-fisca-simu-etat DEBUG @ 20:10:49] Temps de traitement total pour la simulation 7.873102587996982 secondes\n\n\n```python\nprint(\n    f"Montant total de la csg : {resultat.result[\'amendement\'].state_budget[\'csg\']:,} €"\n)\n```\n\n    Montant total de la csg : -147,054,542,277.62744 €\n\n\n# How to develop\n\nPlease see contributing.\n',
    'author': 'Leximpact',
    'author_email': 'Leximpact@an.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://simulateur-socio-fisca.leximpact.dev/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
