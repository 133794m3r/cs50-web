Paddle = Class{}

function Paddle:init(x,y,width,height)
	self.x=x
	self.y=y
	self.width=width
	self.height=height
	self.dy=0
end

function Paddle:update(dt)

	if self.dy < 0 then
		self.y = math.max(0,self.y+self.dy*dt)
	else
		self.y = math.min(VIRTUAL_HEIGHT - self.height, self.y+self.dy*dt)
	end
end

function Paddle:draw()
    love.graphics.rectangle('fill', self.x, self.y, self.width, self.height)
end

Ai = Class{}


function Ai:init(level, move_speed)
	self.level = level
	self.move_speed = move_speed
	self.cur_bonus = 0
	self.mid = 10
end


function Ai:update(dt)
	dt=dt*1.5
	if math.random(2) == 1 then
		return false;
	end
	if ball.y > player2.y then
		player2.y = ball.y
	elseif ball.y < player2.y then
		player2.y = ball.y
	end

	if player2.y < 0 then
		player2.y = 0
	else
		player2.y = math.min(VIRTUAL_HEIGHT - player2.height,player2.y)
	end
	player2.dy = 0
end
