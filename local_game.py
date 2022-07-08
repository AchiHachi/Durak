from render import ConsoleRenderer
from Durak import Durak


class Game:
    def __init__(self, rng):
        self.rng = rng

    def local_game(self):

        game = Durak(self.rng)
        renderer = ConsoleRenderer()

        renderer.help()

        while not game.winner:
            renderer.render_game(game, my_index=0)

            renderer.sep()
            choice = input('Ваш выбор: ')
            # разбиваем на части: команда - пробел - номер карты
            parts = choice.lower().split(' ')
            if not parts:
                break

            command = parts[0]

            try:
                if command == 'f':
                    r = game.finish_turn()
                    print(f'Ход окончен: {r}')
                elif command == 'a':
                    index = int(parts[1]) - 1
                    card = game.current_player[index]
                    if not game.attack(card):
                        print('Вы не можете ходить с этой карты!')
                elif command == 'd':
                    index = int(parts[1]) - 1
                    new_card = game.opponent_player[index]

                    # варианты защиты выбранной картой
                    variants = game.defend_variants(new_card)

                    if len(variants) == 1:
                        def_index = variants[0]
                    else:
                        def_index = int(input(f'Какую позицию отбить {new_card}? ')) - 1
                    old_card = list(game.field.keys())[def_index]
                    if not game.defend(old_card, new_card):
                        print('Не можете так отбиться')
                elif command == 'q':
                    print('QUIT!')
                    break
            except IndexError:
                print('Неправильный выбор карты')
            except ValueError:
                print('Введите число через пробел после команды')

            if game.winner:
                print(f'Игра окончена, победитель игрок: #{game.winner + 1}')
                break
