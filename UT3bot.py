#201401061, 201425095

import random
import math
import time

class Player54:
	def __init__(self):
		# You may initialize your object here and use any variables for storing throughout the game
		self.depth_limit = 4
		self.player = 'o'
		self.opp = 'x'
		self.best_move = (-1,-1)
		self.block_utility = [0]*9
		self.timed_out_best_move = (-1,-1)
		pass

	def move(self,temp_board,temp_block,old_move,flag):
#		print "entered"
		if old_move == (-1,-1):
#			print "swg"
			self.player = 'x'
		       	self.opp = 'o'
		temp_game_board = temp_board[:]
		temp_block_st = temp_block[:]
#		blocks_allowed = self.determine_blocks_allowed(old_move, temp_block_st)
#		cells = self.get_empty_out_of(temp_game_board, blocks_allowed, temp_block_st)
#		return cells[random.randrange(len(cells))]
#		print 'hey'
		t = self.alphabeta_search(old_move, temp_game_board, temp_block_st, 0, float('-inf') , float('inf'), self.player)
#		best_utility = t[0]
		self.best_move = t[1]
#		print "______________________"
#		print best_utility
#		print 'yeah'
#		print "team54"
#		print self.best_move
#		print "yayy"
		return self.best_move

	def determine_blocks_allowed(self,old_move, block_stat):
		blocks_allowed = []
		old_move_0 = old_move[0] % 3
		old_move_1 = old_move[1] % 3
		if old_move_0 == 1 and old_move_1== 1 and block_stat[4] == '-':
			blocks_allowed = [4]
		elif old_move_0 == 1:
			if block_stat[3*(old_move_0-1)+old_move_1] == '-':
				blocks_allowed.append(3*(old_move_0-1)+old_move_1)
			if block_stat[3*(old_move_0+1)+old_move_1] == '-':
				blocks_allowed.append(3*(old_move_0+1)+old_move_1)
		elif old_move_1 == 1:
			if block_stat[3*(old_move_0)+old_move_1-1] == '-':
				blocks_allowed.append(3*(old_move_0)+old_move_1-1)
			if block_stat[3*(old_move_0)+old_move_1+1] == '-':
				blocks_allowed.append(3*(old_move_0)+old_move_1+1)
		elif old_move_0 == 0:
			if block_stat[3*(old_move_0+1)+old_move_1] == '-':
				blocks_allowed.append(3*(old_move_0+1)+old_move_1)
			if block_stat[3*(old_move_0)+1] == '-':
				blocks_allowed.append(3*(old_move_0)+1)
		else:
			if block_stat[3*(old_move_0-1)+old_move_1] == '-':
				blocks_allowed.append(3*(old_move_0-1)+old_move_1)
			if block_stat[3*(old_move_0)+1] == '-':
				blocks_allowed.append(3*(old_move_0)+1)
		return blocks_allowed

	def get_empty_out_of(self, temp_game_board, blal, block_stat):
		cells = []  # it will be list of tuples
		if blal != []:
			for i in blal:
				for j in range(3):
					for k in range(3):
						if (temp_game_board[j+3*(i/3)][k+3*(i%3)] == '-'):
							cells.append((j+3*(i/3),k+3*(i%3)))
		else:
			for i in range(9):
				if block_stat[i] == '-':
					for j in range(3):
						for k in range(3):
							if (temp_game_board[j+3*(i/3)][k+3*(i%3)] == '-'):
								cells.append((j+3*(i/3),k+3*(i%3)))
		return cells

	def alphabeta_search(self, old_move, temp_game_board, temp_block_st, depth, alpha, beta, pl):
#		tgb = temp_game_board[:]
		tbs = temp_block_st[:]
#		print depth
#		return 1
#		print "yo"
		if(depth >= self.depth_limit or self.terminal_state_reached(temp_game_board, temp_block_st)):
#			if depth > self.depth_limit:
#				print "depth exceeded"
#			if self.terminal_state_reached(temp_game_board, temp_block_st):
#				print"TERMINAL"
#			print "terminal"
			return (self.eval_func(temp_game_board, temp_block_st), old_move)
		blocks_allowed = self.determine_blocks_allowed(old_move, temp_block_st)
#		print blocks_allowed
#		time.sleep(10)
		cells = self.get_empty_out_of(temp_game_board, blocks_allowed, temp_block_st)
#		if cells == []:
#			print "empty"
#		print pl
		best_move = cells[0]
		if pl == self.player:
#			print "me"
			for i in cells:
#				print depth
#				print "hey"
#				print i
#				old_move = i
				self.update_lists(temp_game_board, temp_block_st, i, pl)
#				print "boo"
				t = self.alphabeta_search(i, temp_game_board, temp_block_st, depth+1, alpha, beta, self.opp)
#				print t
				v = t[0]
				temp_game_board[i[0]][i[1]] = '-'
				temp_block_st = tbs[:]
				if v > alpha:
					alpha = v
					best_move = i
#				print "boo"
#				print "after me"
#				print depth
				if alpha >= beta:
#					print "prune"
					break
#				return alpha
			return (alpha, best_move)
		else:
#			print "opponent"
			for i in cells:
#				print depth
#				print "hi"
#				print i
#				old_move = i
				self.update_lists(temp_game_board, temp_block_st, i, pl)
				t = self.alphabeta_search(i, temp_game_board, temp_block_st, depth+1, alpha, beta, self.player)
				v = t[0]
				temp_game_board[i[0]][i[1]] = '-'
				temp_block_st = tbs[:]
				if v < beta:
					beta = v
					best_move = i
#				print "bee"
#				print "boo"
#				print "after opp"
#				print depth
				if alpha >= beta:
#					print "prune"
					break
#				return beta
			return (beta, best_move)
#		print "end"

	def compute_block_utility (self, temp_game_board, temp_block_st):
#		print "bu"
		for i in range(9):
#			print "goo"
#			self.block_utility[i] = 0
			if temp_block_st[i] == self.player:
				self.block_utility[i] = 100
#				print "i win"
			elif temp_block_st[i] == self.opp:
				self.block_utility[i] = -100
#				print "you win"
			elif temp_block_st[i] == 'D':
				self.block_utility[i] = 0
#				print "draw"
			if temp_block_st[i] == '-':
#				print "not won yet"
				self.block_utility[i] = 0
#				max_utility = float('-inf')
#				min_utility = float('inf')
				for j in range(3):
#					print "poo"
					row_no_of_x = 0
					row_no_of_o = 0
					col_no_of_x = 0
					col_no_of_o = 0
#					diag_no_of_x = 0
#					diag_no_of_o = 0
#					row_utility = float('-inf')
#					column_utility = float('-inf')
#					diagonal_utility = float('-inf')
#					print "1"
					if (temp_game_board[j+3*(i/3)][3*(i%3)] == 'x'):
						row_no_of_x += 1
					elif (temp_game_board[j+3*(i/3)][3*(i%3)] == 'o'):
						row_no_of_o += 1
#					print "lala"
					if (temp_game_board[j+3*(i/3)][3*(i%3)+1] == 'x'):
						row_no_of_x += 1
					elif (temp_game_board[j+3*(i/3)][3*(i%3)+1] == 'o'):
						row_no_of_o += 1
					if (temp_game_board[j+3*(i/3)][3*(i%3)+2] == 'x'):
						row_no_of_x += 1
					elif (temp_game_board[j+3*(i/3)][3*(i%3)+2] == 'o'):
						row_no_of_o += 1
#					print "2"
					if (temp_game_board[3*(i/3)][j+3*(i%3)] == 'x'):
						col_no_of_x += 1
					elif (temp_game_board[3*(i/3)][j+3*(i%3)] == 'o'):
						col_no_of_o += 1
					if (temp_game_board[3*(i/3) + 1][j+3*(i%3)] == 'x'):
						col_no_of_x += 1
					elif (temp_game_board[3*(i/3) + 1][j+3*(i%3)] == 'o'):
						col_no_of_o += 1
					if (temp_game_board[3*(i/3) + 2][j+3*(i%3)] == 'x'):
						col_no_of_x += 1
					elif (temp_game_board[3*(i/3) + 2][j+3*(i%3)] == 'o'):
						col_no_of_o += 1
#					print "3"
					if j < 2:
						delta_x = 0
						if j == 0:
							delta_y = 0
						else:
							delta_y = 2
						diag_no_of_x = 0
						diag_no_of_o = 0
#						print "diag"
						for k in range(3):
#							print "inside"
#							print "hey"
#							print i
#							print j
#							print 3*(i/3) + delta_x
#							print 3*(i%3) + delta_y + st
							if (temp_game_board[3*(i/3) + delta_x][3*(i%3) + delta_y] == 'x'):
								diag_no_of_x += 1
							elif (temp_game_board[3*(i/3) + delta_x][3*(i%3) + delta_y] == 'o'):
								diag_no_of_o += 1
#							print "yo"
							delta_x += 1
							delta_y += pow(-1,j)
						if self.player == 'x':
							if diag_no_of_o == 0 and diag_no_of_x != 0:
								diagonal_utility = pow(10,diag_no_of_x -1)
							elif diag_no_of_x == 0 and diag_no_of_o != 0:
								diagonal_utility = -pow(10,diag_no_of_o - 1)
							else:
								diagonal_utility = 0
						else:
							if diag_no_of_x == 0 and diag_no_of_o != 0:
								diagonal_utility = pow(10,diag_no_of_o - 1)
							elif diag_no_of_o == 0 and diag_no_of_x != 0:
								diagonal_utility = -pow(10,diag_no_of_x - 1)
							else:
								diagonal_utility = 0
						self.block_utility[i] += diagonal_utility
#						print "4"
#						if diagonal_utility > max_utility:
#							max_utility = diagonal_utility
#						print "5"
#						if diagonal_utility < min_utility:
#							min_utility = diagonal_utility
#						print "6"
#						print diagonal_utility
#						self.block_utility[i] += diagonal_utility
#						print "pee"
					if self.player == 'x':
						if row_no_of_o == 0 and row_no_of_x != 0:
							row_utility = pow(10,row_no_of_x -1)
						elif row_no_of_x == 0 and row_no_of_o != 0:
							row_utility = -pow(10,row_no_of_o - 1)
						else:
							row_utility = 0
						if col_no_of_o == 0 and col_no_of_x != 0:
							column_utility = pow(10,col_no_of_x -1)
						elif col_no_of_x == 0 and col_no_of_o != 0:
							column_utility = -pow(10,col_no_of_o - 1)
						else:
							column_utility = 0
					else:
						if row_no_of_x == 0 and row_no_of_o != 0:
							row_utility = pow(10,row_no_of_o - 1)
						elif row_no_of_o == 0 and row_no_of_x != 0:
							row_utility = -pow(10,row_no_of_x - 1)
						else:
							row_utility = 0
						if col_no_of_x == 0 and col_no_of_o != 0:
							column_utility = pow(10,col_no_of_o - 1)
						elif col_no_of_o == 0 and col_no_of_x != 0:
							column_utility = -pow(10,col_no_of_x - 1)
						else:
							column_utility = 0
					self.block_utility[i] += (row_utility+column_utility)
#					if row_utility < min_utility:
#						min_utility = row_utility
#					if column_utility < min_utility:
#						min_utility = column_utility
#					if row_utility > max_utility:
#						max_utility = row_utility
#					print "poop"
#					if column_utility > max_utility:
#						max_utility = column_utility
#					self.block_utility[i] += (column_utility + row_utility)
#			print "boo"
			self.block_utility[i] = float(self.block_utility[i])/100
#			self.block_utility[i] = max_utility/100

	def eval_func(self, temp_game_board, temp_block_st):
		self.compute_block_utility(temp_game_board, temp_block_st)
		final_utility = 0
#		d = {0:3,1:2,2:3,3:2,4:4,5:2,6:3,7:2,8:3}
		possible_win_sequences = [(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
		for i in possible_win_sequences:
			pl = 0
			opp = 0
			none = 0
			sum_p = 0
			for j in i:
				if self.block_utility[j] == 1:
					pl += 1
				elif self.block_utility[j] == -1:
					opp += 1
				elif self.block_utility[j] != 0:
					none += 1
					sum_p += self.block_utility[j]
				if pl == 3:
					return 1000
				elif opp == 3:
					return -1000
				if pl != 0:
					final_utility += pow(10,pl - 1)
				if opp != 0:
					final_utility -= pow(10,opp - 1)
				if none != 0:
					final_utility += (sum_p*pow(10,none - 1))
		return final_utility
# #
#		for i in range(3):
#			row_no_of_pl = 0
#			row_no_of_op = 0
#			col_no_of_pl = 0
#			col_no_of_op = 0
#			row_no_of_none = 0
#			col_no_of_none = 0
#			row_sum_bl = 0
#			col_sum_bl = 0
#			if self.block_utility[3*i] == 1:
#				row_no_of_pl += 1
#			elif self.block_utility[3*i] == -1:
#				row_no_of_op += 1
#			elif self.block_utility[3*i] != 0:
#				row_no_of_none += 1
#				row_sum_bl += self.block_utility[3*i]
#			if self.block_utility[3*i + 1] == 1:
#				row_no_of_pl += 1
#			elif self.block_utility[3*i + 1] == -1:
#				row_no_of_op += 1
#			elif self.block_utility[3*i + 1] != 0:
#				row_no_of_none += 1
#				row_sum_bl += self.block_utility[3*i + 1]
#			if self.block_utility[3*i + 2] == 1:
#				row_no_of_pl += 1
#			elif self.block_utility[3*i + 2] == -1:
#				row_no_of_op += 1
#			elif self.block_utility[3*i + 2] != 0:
#				row_no_of_none += 1
#				row_sum_bl += self.block_utility[3*i + 2]
#			if self.block_utility[i] == 1:
#				col_no_of_pl += 1
#			elif self.block_utility[i] == -1:
#				col_no_of_op += 1
#			elif self.block_utility[i] != 0:
#				col_no_of_none += 1
#				col_sum_bl += self.block_utility[i]
#			if self.block_utility[i + 3] == 1:
#				col_no_of_pl += 1
#			elif self.block_utility[i + 3] == -1:
#				col_no_of_op += 1
#			elif self.block_utility[i + 3] != 0:
#				col_no_of_none += 1
#				col_sum_bl += self.block_utility[i + 3]
#			if self.block_utility[i + 6] == 1:
#				col_no_of_pl += 1
#			elif self.block_utility[i + 6] == -1:
#				col_no_of_op += 1
#			elif self.block_utility[i + 6] != 0:
#				col_no_of_none += 1
#				col_sum_bl += self.block_utility[i + 6]
# #			if row_no_of_pl == 3:
# #				return 100
# #			elif row_no_of_op == 3:
# #				return -100
#			if row_no_of_pl != 0:
#				final_utility += pow(10,row_no_of_pl - 1)
#			if row_no_of_op != 0:
#				final_utility += (-pow(10,row_no_of_op - 1))
#			if col_no_of_pl != 0:
#				final_utility += pow(10,col_no_of_pl - 1)
#			if col_no_of_op != 0:
#				final_utility += (-pow(10,col_no_of_op - 1))
#			if row_no_of_none != 0:
#				final_utility += (pow(10,row_no_of_none - 1)* row_sum_bl)
#			if col_no_of_none != 0:
#				final_utility += (pow(10,col_no_of_none - 1)* col_sum_bl)
#		diag_no_of_pl = 0
#		diag_no_of_op = 0
#		diag_no_of_none = 0
#		diag_sum_bl = 0
#		for i in (0,4,8):
#			if self.block_utility[i] == 1:
#				diag_no_of_pl += 1
#			elif self.block_utility[i] == -1:
#				diag_no_of_op += 1
#			elif self.block_utility[i] != 0:
#				diag_no_of_none += 1
#				diag_sum_bl += self.block_utility[i]
# #		if diag_no_of_pl == 3:
# #			return 100
# #		elif diag_no_of_op == 3:
# #			return -100
#		if diag_no_of_pl != 0:
#			final_utility += pow(10, diag_no_of_pl - 1)
#		if diag_no_of_op != 0:
#			final_utility += (-pow(10, diag_no_of_op - 1))
#		if diag_no_of_none != 0:
#			final_utility += (pow(10,diag_no_of_none - 1)*diag_sum_bl)
#		diag_no_of_pl = 0
#		diag_no_of_op = 0
#		diag_no_of_none = 0
#		diag_sum_bl = 0
#		for i in (2,4,6):
#			if self.block_utility[i] == 1:
#				diag_no_of_pl += 1
#			elif self.block_utility[i] == -1:
#				diag_no_of_op += 1
#			elif self.block_utility[i] != 0:
#				diag_no_of_none += 1
#				diag_sum_bl += self.block_utility[i]
# #		if diag_no_of_pl == 3:
# #			return 100
# #		elif diag_no_of_op == 3:
# #			return -100
#		if diag_no_of_pl != 0:
#			final_utility += (pow(10, diag_no_of_pl - 1))
#		if diag_no_of_op != 0:
#			final_utility += (-pow(10, diag_no_of_op - 1))
#		if diag_no_of_none != 0:
#			final_utility += (pow(10,diag_no_of_none - 1)*diag_sum_bl)
# #		print final_utility
#		return final_utility
#		for i in range(3):
#			x = self.block_utility[3*i] + self.block_utility[3*i + 1] + self.block_utility[3*i + 2]
#			if x > 0:
#				j = 0
#			else:
#				j = 1
#			if 1 < abs(x) and abs(x) < 2:
#				final_utility += ((1 + (abs(x) - 1)*(10 - 1))*pow(-1,j))
#			elif 2 < abs(x) and abs(x) < 3:
#				final_utility += ((2 + (abs(x) - 2)*(100 - 10))*pow(-1,j))
#			elif x == 3:
#				return 1000
#			elif x == -3:
#				return -1000
#			else:
#				final_utility += x*(pow(-1,j))
#			x = self.block_utility[i] + self.block_utility[i + 3] + self.block_utility[i + 6]
#			if x > 0:
#				j = 0
#			else:
#				j = 1
#			if 1 < abs(x) and abs(x) < 2:
#				final_utility += ((1 + (abs(x) - 1)*(10 - 1))*pow(-1,j))
#			elif 2 < abs(x) and abs(x) < 3:
#				final_utility += ((2 + (abs(x) - 2)*(100 - 10))*pow(-1,j))
#			elif x == 3:
#				return 1000
#			elif x == -3:
#				return -1000
#			else:
#				final_utility += x*(pow(-1,j))
#		x = self.block_utility[0] + self.block_utility[4] + self.block_utility[8]
#		if x > 0:
#			j = 0
#		else:
#			j = 1
#		if 1 < abs(x) and abs(x) < 2:
#			final_utility += ((1 + (abs(x) - 1)*(10 - 1))*pow(-1,j))
#		elif 2 < abs(x) and abs(x) < 3:
#			final_utility += ((2 + (abs(x) - 2)*(100 - 10))*pow(-1,j))
#		elif x == 3:
#			return 1000
#		elif x == -3:
#			return -1000
#		else:
#			final_utility += x*(pow(-1,j))
#		x = self.block_utility[2] + self.block_utility[4] + self.block_utility[6]
#		if x > 0:
#			j = 0
#		else:
#			j = 1
#		if 1 < abs(x) and abs(x) < 2:
#			final_utility += ((1 + (abs(x) - 1)*(10 - 1))*pow(-1,j))
#		elif 2 < abs(x) and abs(x) < 3:
#			final_utility += ((2 + (abs(x) - 2)*(100 - 10))*pow(-1,j))
#		elif x == 3:
#			return 1000
#		elif x == -3:
#			return -1000
#		else:
#			final_utility += x*(pow(-1,j))
#		return final_utility

	def update_lists(self, temp_game_board, temp_block_st, temp_move_ret, temp_fl):
		temp_game_board[temp_move_ret[0]][temp_move_ret[1]] = temp_fl

		block_no = (temp_move_ret[0]/3)*3 + temp_move_ret[1]/3
		id1 = block_no/3
		id2 = block_no%3
		mflg = 0

		flag = 0
		for i in range(id1*3,id1*3+3):
			for j in range(id2*3,id2*3+3):
				if temp_game_board[i][j] == '-':
					flag = 1

		if temp_block_st[block_no] == '-':
			if temp_game_board[id1*3][id2*3] == temp_game_board[id1*3+1][id2*3+1] and temp_game_board[id1*3+1][id2*3+1] == temp_game_board[id1*3+2][id2*3+2] and temp_game_board[id1*3+1][id2*3+1] != '-' and temp_game_board[id1*3+1][id2*3+1] != 'D':
				mflg=1
			if temp_game_board[id1*3+2][id2*3] == temp_game_board[id1*3+1][id2*3+1] and temp_game_board[id1*3+1][id2*3+1] == temp_game_board[id1*3][id2*3 + 2] and temp_game_board[id1*3+1][id2*3+1] != '-' and temp_game_board[id1*3+1][id2*3+1] != 'D':
				mflg=1
			if mflg != 1:
			    for i in range(id2*3,id2*3+3):
			        if temp_game_board[id1*3][i]== temp_game_board[id1*3+1][i] and temp_game_board[id1*3+1][i] == temp_game_board[id1*3+2][i] and temp_game_board[id1*3][i] != '-' and temp_game_board[id1*3][i] != 'D':
			                mflg = 1
			                break
			if mflg != 1:
			    for i in range(id1*3,id1*3+3):
			        if temp_game_board[i][id2*3]== temp_game_board[i][id2*3+1] and temp_game_board[i][id2*3+1] == temp_game_board[i][id2*3+2] and temp_game_board[i][id2*3] != '-' and temp_game_board[i][id2*3] != 'D':
			                mflg = 1
			                break
		if flag == 0:
			temp_block_st[block_no] = 'D'
		if mflg == 1:
			temp_block_st[block_no] = temp_fl

	#Check win
	def terminal_state_reached(self, temp_game_board, temp_block_st):
		### we are now concerned only with block_stat
#		bs = temp_block_st
		## Row win
		if (temp_block_st[0] == temp_block_st[1] and temp_block_st[1] == temp_block_st[2] and temp_block_st[1]!='-' and temp_block_st[1]!='D') or (temp_block_st[3]!='-' and temp_block_st[3]!='D' and temp_block_st[3] == temp_block_st[4] and temp_block_st[4] == temp_block_st[5]) or (temp_block_st[6]!='D' and temp_block_st[6]!='-' and temp_block_st[6] == temp_block_st[7] and temp_block_st[7] == temp_block_st[8]):
			return True
		## Col win
		elif (temp_block_st[0] == temp_block_st[3] and temp_block_st[3] == temp_block_st[6] and temp_block_st[0]!='-' and temp_block_st[0]!='D') or (temp_block_st[1] == temp_block_st[4] and temp_block_st[4] == temp_block_st[7] and temp_block_st[4]!='-' and temp_block_st[4]!='D') or (temp_block_st[2] == temp_block_st[5] and temp_block_st[5] == temp_block_st[8] and temp_block_st[5]!='-' and temp_block_st[5]!='D'):
			return True
		## Diag win
		elif (temp_block_st[0] == temp_block_st[4] and temp_block_st[4] == temp_block_st[8] and temp_block_st[0]!='-' and temp_block_st[0]!='D') or (temp_block_st[2] == temp_block_st[4] and temp_block_st[4] == temp_block_st[6] and temp_block_st[2]!='-' and temp_block_st[2]!='D'):
			return True
		else:
			smfl = 0
			for i in range(9):
				if temp_block_st[i] == '-':
					return False
			return True
