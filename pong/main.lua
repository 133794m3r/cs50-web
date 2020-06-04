push = require "push"
Class = require "class"
require "Ball"
require "Paddle"

WINDOW_HEIGHT=720
WINDOW_WIDTH=1280
VIRTUAL_WIDTH = 432
VIRTUAL_HEIGHT = 243
PADDLE_SPEED=200
SCORE_1_X=VIRTUAL_WIDTH/2-50
SCORE_2_X=VIRTUAL_WIDTH/2+30
SCORE_Y=VIRTUAL_HEIGHT/3
AI_TICK=0.05
AI_TICK_DELAY=AI_TICK
function reset_state()
	player_1_score=0
	player_2_score=0
	ball = Ball(VIRTUAL_WIDTH/2 -2, VIRTUAL_HEIGHT/2 -2, 4, 4)
	player1 = Paddle(10, 30, 5, 20)
	player2 = Paddle(VIRTUAL_WIDTH -15, VIRTUAL_HEIGHT - 20, 5, 20)
	game_type = 1
end
function love.load()
	love.graphics.setDefaultFilter("nearest","nearest")
	
	small_font=love.graphics.newFont("font.ttf",8)
	score_font=love.graphics.newFont("font.ttf",32)
	love.graphics.setFont(small_font)
	math.randomseed(os.time())
	push:setupScreen(VIRTUAL_WIDTH, VIRTUAL_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, {
		fullscreen = false,
	 	resizable = true,
		vsync = true
	})
	sounds = {
		['paddle_hit'] = love.audio.newSource('sounds/paddle_hit.wav', 'static'),
		['score'] = love.audio.newSource('sounds/score.wav', 'static'),
		['wall_hit'] = love.audio.newSource('sounds/wall_hit.wav', 'static')
	}	
	reset_state()
	
	ai_player = Ai(1,400)
	current_ai_tick = 0
	state="init"
end

function love.resize(w, h)
	push:resize(w, h)
end
function paddle_ai()
	--
end
function love.keypressed(key)
	--AI game mode.
	if key == "1" then
		game_type = 0
		state="start"
	--2 player mode.
	elseif key == "2" then
		game_type = 1
		state="start"
	end
	if key == "escape" then
		love.event.quit()
	elseif key == "enter" or key == "return" then
		if state == "done" then
			state = "play"
			reset_state()
		elseif state == "serve" then
			state = "play"
		elseif state == "start" then
			state = "play"	
		else
			state="start"
			ball:reset()	
		end
	end
end

function love.update(dt)
	if love.keyboard.isDown("w") then
		player1.dy= -PADDLE_SPEED
	elseif love.keyboard.isDown("s") then
		player1.dy = PADDLE_SPEED
	else
		player1.dy=0
	end
	if game_type == 1 then
		if love.keyboard.isDown("up") then
			player2.dy= -PADDLE_SPEED
		elseif love.keyboard.isDown("down") then
			player2.dy = PADDLE_SPEED
		else 
			player2.dy = 0
		end
	end
	if state == "done" then
		
	elseif state == "serve" then
		ball.dy = math.random(-50,50)
		if serve == 1 then
			ball.dx = math.random(100,150) * 1
		else
			ball.dx = math.random(100,150) * -1
		end
	elseif state == "play" then
		if ball:collides(player1) then
			ball.dx = -ball.dx * 1.03
			ball.x = player1.x + 5
			sounds['paddle_hit']:play()			
		elseif ball:collides(player2) then
			ball.dx = -ball.dx * 1.03
			ball.x = player2.x - 4		
			sounds['paddle_hit']:play()			
		end	
		if ball.x < 0 then
			serve=2
			state='serve'
			player_2_score=player_2_score+1
			sounds['score']:play()
			ball:reset()
		elseif ball.x > VIRTUAL_WIDTH then
			serve=1
			state='serve'
			sounds['score']:play()
			player_1_score=player_1_score+1
			ball:reset()
		end
		hit=ball:update(dt);
		if hit then
			sounds['wall_hit']:play()
		end
		if player_1_score == 2 or player_2_score == 2 then
			state="done"
		end
		current_ai_tick = current_ai_tick + dt
		if current_ai_tick >= AI_TICK_DELAY then
			AI_TICK_DELAY=0.1 + (math.random(5)/100)
			ai_player:update(dt)
			current_ai_tick = 0			
		end

	end

	player1:update(dt)
	if game_type == 1 then
		player2:update(dt)
	end
end

function love.draw()
	push:apply("start")
		love.graphics.setFont(small_font)
		if state == 'init' then
			love.graphics.printf("Welcome to Pong!",0,10,VIRTUAL_WIDTH,"center")
			love.graphics.printf("For a 1 player game press 1. For a two player game press 2.",0,20,VIRTUAL_WIDTH,"center")
		elseif state == 'start' then
		 	love.graphics.printf("Welcome to Pong!",0,10,VIRTUAL_WIDTH,'center')
			love.graphics.printf("Press enter to start a " .. tostring(game_type+1) .." game!", 0, 20, VIRTUAL_WIDTH, 'center')
		elseif state == 'serve' then
			love.graphics.printf("Player " .. tostring(serve) .. " is serving",0,10,VIRTUAL_WIDTH,'center')
			love.graphics.printf("Press enter to serve!",0,20,VIRTUAL_WIDTH,'center')
		elseif state == "play" then
			love.graphics.printf("Let's play Pong!", 0, 20, VIRTUAL_WIDTH, 'center')
			--this was a timer so that I could verify thatmy ticks worked.
			--[[
			love.graphics.setFont(small_font)		
			love.graphics.print("Current Timer: " .. tostring(current_ai_tick),VIRTUAL_WIDTH - 200, 10)			
			]]
		elseif state == "done" then
			winner = player_1_score > player_2_score and 1 or 2
			love.graphics.printf("Player " .. tostring(winner) .. " won!",0,10,VIRTUAL_WIDTH,'center')
			love.graphics.printf("Press enter to play again!",0,20,VIRTUAL_WIDTH,'center')
		end

		--player1 paddle
		player1:draw()
		--player2 paddle
		player2:draw()
		--the ball
		ball:draw()
		display_score()
		--some debug information was shown here.
		--[[
		love.graphics.setFont(small_font)
		love.graphics.print("B.dx",0,VIRTUAL_HEIGHT-20)
		love.graphics.print(tostring(math.floor(ball.dx)),30,VIRTUAL_HEIGHT-20)
		love.graphics.print("B.dy",50,VIRTUAL_HEIGHT-20)
		love.graphics.print(tostring(math.floor(ball.dy)),70,VIRTUAL_HEIGHT-20)
		]]
		fps_counter()
	push:apply("end")
end
function display_score()
	love.graphics.setFont(score_font)
	love.graphics.print(tostring(player_1_score),SCORE_1_X,SCORE_Y)
	love.graphics.print(tostring(player_2_score),SCORE_2_X,SCORE_Y)	
end
function fps_counter()
	love.graphics.setFont(small_font)
	love.graphics.setColor(0,255,0,255)
	love.graphics.print("FPS: " .. tostring(love.timer.getFPS()),10,10)
end
