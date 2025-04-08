import unittest

from names_dataset import NameDataset
from names_dataset.emails import extract_names_from_email, try_to_split_with_two_last_names


class TestEmail(unittest.TestCase):

    def test_bugs_1(self):
        # http://philipperemy.ddns.net:9999/split?q=remy.p@gmail.com
        # http://philipperemy.ddns.net:9999/split?q=p.remy@gmail.com
        # It seems that always expect at least 2 parameters.
        # If you try: http://philipperemy.ddns.net:9999/split?q=premy@gmail.com it works but not form
        # http://philipperemy.ddns.net:9999/split?q=pr@gmail.com
        # or
        # http://philipperemy.ddns.net:9999/split?q=Remy@gmail.com
        inputs = [
            'remy.p@gmail.com',
            'p.remy@gmail.com',
            'Remy@gmail.com'
        ]

        outputs = [
            ['remy', None],
            [None, 'remy'],
            ['remy', None],
        ]

        outputs2 = [
            ['remy', None, None],
            ['remy', None, None],
            ['remy', None, None],
            ['remy', None, None],
        ]

        nd = NameDataset()
        for input_, output_, output2_ in zip(inputs, outputs, outputs2):
            first_name, last_name = extract_names_from_email(nd, input_)
            print(input_)
            print('output=', first_name, last_name)
            print('expected=', output_[0], output_[1])
            self.assertEqual(output_[0], first_name)
            self.assertEqual(output_[1], last_name)

            first_name, last_name, last_name2 = try_to_split_with_two_last_names(nd, input_)

            self.assertEqual(output2_[0], first_name)
            self.assertEqual(output2_[1], last_name)
            self.assertEqual(output2_[2], last_name2)
            print('[OK]')

    def test_with_three_3(self):
        inputs = [
            'perezmartiisabel',
            'isabelmartiperez',
            'martiperezisabel',
            'isabelperezmarti',

            'garciafernandezmaria',
            'mariafernandezgarcia',

            'gonzalezlopezana',
            'analopezgonzalez',

            'rodriguezhernandezjuan',
            'juanhernandezrodriguez',

            'suarezdominguezcarlos',
            'carlosdominguezsuarez',

            'sanchezruizlucia',
            'luciaruizsanchez',

            'gomeznunezmiguel',
            'miguelnunezgomez',

        ]

        outputs = [
            ['isabel', 'perez', 'marti'],
            ['isabel', 'marti', 'perez'],
            ['isabel', 'marti', 'perez'],
            ['isabel', 'perez', 'marti'],

            ['maria', 'garcia', 'fernandez'],
            ['maria', 'fernandez', 'garcia'],

            ['ana', 'gonzalez', 'lopez'],
            ['ana', 'lopez', 'gonzalez'],

            ['juan', 'rodriguez', 'hernandez'],
            ['juan', 'hernandez', 'rodriguez'],

            ['carlos', 'suarez', 'dominguez'],
            ['carlos', 'dominguez', 'suarez'],

            ['lucia', 'sanchez', 'ruiz'],
            ['lucia', 'ruiz', 'sanchez'],

            ['miguel', 'gomez', 'nunez'],
            ['miguel', 'nunez', 'gomez'],
        ]
        inputs2 = []
        for i in inputs:
            inputs2.append(i.split('@')[0])

        nd = NameDataset()
        for input_, output_ in zip(inputs2, outputs):
            first_name, last_name, last_name2 = try_to_split_with_two_last_names(nd, input_)
            print(input_)
            print('output=', first_name, last_name, last_name2)
            print('expected=', output_[0], output_[1], output_[2])
            self.assertEqual(output_[0], first_name)
            self.assertEqual(output_[1], last_name)
            self.assertEqual(output_[2], last_name2)
            print('[OK]')

    def test_with_three_2(self):
        inputs = [
            'torresmoralesines',

            'perezmartiisabel',
            'isabelmartiperez',
            'martiperezisabel',
            'isabelperezmarti',

            'garciafernandezmaria',
            'mariafernandezgarcia',
            'fernandezgarciamaria',
            'mariagarciafernandez',

            'gonzalezlopezana',
            'analopezgonzalez',
            'lopezgonzalezana',
            'anagonzalezlopez',

            'rodriguezhernandezjuan',
            'juanhernandezrodriguez',
            'hernandezrodriguezjuan',
            'juanrodriguezhernandez',

            'suarezdominguezcarlos',
            'carlosdominguezsuarez',
            'dominguezsuarezcarlos',
            'carlossuarezdominguez',

            'sanchezruizlucia',
            'luciaruizsanchez',
            'ruizsanchezlucia',
            'luciasanchezruiz',

            'gomeznunezmiguel',
            'miguelnunezgomez',
            'nunezgomezmiguel',
            'miguelgomeznunez',

            'moralestorresines',
            'inestorresmorales',
        ]

        outputs = [
            ['ines', 'torres', 'morales'],

            ['isabel', 'perez', 'marti'],
            ['isabel', 'marti', 'perez'],
            ['isabel', 'marti', 'perez'],
            ['isabel', 'perez', 'marti'],

            ['maria', 'garcia', 'fernandez'],
            ['maria', 'fernandez', 'garcia'],
            ['maria', 'fernandez', 'garcia'],
            ['maria', 'garcia', 'fernandez'],

            ['ana', 'gonzalez', 'lopez'],
            ['ana', 'lopez', 'gonzalez'],
            ['ana', 'lopez', 'gonzalez'],
            ['ana', 'gonzalez', 'lopez'],

            ['juan', 'rodriguez', 'hernandez'],
            ['juan', 'hernandez', 'rodriguez'],
            ['juan', 'hernandez', 'rodriguez'],
            ['juan', 'rodriguez', 'hernandez'],

            ['carlos', 'suarez', 'dominguez'],
            ['carlos', 'dominguez', 'suarez'],
            ['carlos', 'dominguez', 'suarez'],
            ['carlos', 'suarez', 'dominguez'],

            ['lucia', 'sanchez', 'ruiz'],
            ['lucia', 'ruiz', 'sanchez'],
            ['lucia', 'ruiz', 'sanchez'],
            ['lucia', 'sanchez', 'ruiz'],

            ['miguel', 'gomez', 'nunez'],
            ['miguel', 'nunez', 'gomez'],
            ['miguel', 'nunez', 'gomez'],
            ['miguel', 'gomez', 'nunez'],

            ['ines', 'morales', 'torres'],
            ['ines', 'torres', 'morales'],
        ]
        inputs2 = []
        for i in inputs:
            inputs2.append(i.split('@')[0])

        nd = NameDataset()
        for input_, output_ in zip(inputs2, outputs):
            first_name, last_name, last_name2 = try_to_split_with_two_last_names(nd, input_)
            print(input_)
            print('output=', first_name, last_name, last_name2)
            print('expected=', output_[0], output_[1], output_[2])
            self.assertEqual(output_[0], first_name)
            self.assertEqual(output_[1], last_name)
            self.assertEqual(output_[2], last_name2)
            print('[OK]')

    def test_with_three_1(self):
        inputs = [
            'perezmartiisabel',
            'isabelmartiperez',
            'martiperezisabel',
            'isabelperezmarti',
        ]
        outputs = [
            ['isabel', 'perez', 'marti'],
            ['isabel', 'marti', 'perez'],

            ['isabel', 'marti', 'perez'],
            ['isabel', 'perez', 'marti'],
        ]
        inputs2 = []
        for i in inputs:
            inputs2.append(i.split('@')[0])

        nd = NameDataset()
        for input_, output_ in zip(inputs2, outputs):
            first_name, last_name, last_name2 = try_to_split_with_two_last_names(nd, input_)
            print(input_)
            print('output=', first_name, last_name, last_name2)
            self.assertEqual(output_[0], first_name)
            self.assertEqual(output_[1], last_name)
            self.assertEqual(output_[2], last_name2)
            print('[OK]')

    def test_with_two(self):
        inputs = [
            'info@skysense.jp',
            'isabelle.remy.fr@gmail.com',
            'philippe.remy@example.com',
            'philipperemy@example.com',
            'philippe.d@example.com',
            'p.remy123@example.com',
            'philippe@example.com',
            'philippe_remy@example.com',
            'remy.philippe@example.com',
            'remyphilippe@example.com',
            'j_remy@example.com',
            'philippe.remy123@example.com',
            'philippe.d@example.com',
            'philippe.d@example.com',
            'j.remy@example.com',
            'remyphilippe123@example.com',
            'philippe-d@example.com',
            'remy_j@example.com',
            'j_remy123@example.com',
            'philippe.remy1@example.com',
            'perezmarti',
        ]
        inputs2 = []
        for i in inputs:
            inputs2.append(i.split('@')[0])

        outputs = [
            [None, None],
            ['isabelle', 'remy'],
            ['philippe', 'remy'],
            ['philippe', 'remy'],
            ['philippe', None],
            [None, 'remy'],
            ['philippe', None],
            ['philippe', 'remy'],
            ['philippe', 'remy'],
            ['philippe', 'remy'],
            [None, 'remy'],
            ['philippe', 'remy'],
            ['philippe', None],
            ['philippe', None],
            [None, 'remy'],
            ['philippe', 'remy'],
            ['philippe', None],
            ['remy', None],
            [None, 'remy'],
            ['philippe', 'remy'],
            ['perez', 'marti'],
        ]

        nd = NameDataset()
        for input_, output_ in zip(inputs2, outputs):
            first_name, last_name = extract_names_from_email(nd, input_)
            print(input_)
            self.assertEqual(output_[0], first_name)
            self.assertEqual(output_[1], last_name)
            print('[OK]')
