class GameStats:
	"""ВІдстежуймо статистику гри"""

	def __init__(self, ai_game):
		"""Ініціалізуємо статистику"""
		self.high_score = 0

		#Налаштування
		self.settings = ai_game.settings
		self.reset_stats()
		self.game_active = False

	def reset_stats(self):
		self.ships_left = self.settings.ships_limit
		self.score = 0
		self.current_level = 1