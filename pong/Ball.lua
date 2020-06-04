Ball = Class{}

function Ball:init(x,y,width,height)
	self.x = x
	self.y = y
	self.width = width
	self.height = height
	
	self.dx=math.random(2) == 1 and 100 or -100
    self.dy = math.random(-50,50) * 1.5
    
end

function Ball:reset()
    self.x = VIRTUAL_WIDTH / 2 - 2
    self.y = VIRTUAL_HEIGHT / 2 - 2
    self.dy = math.random(2) == 1 and -100 or 100
    self.dx = math.random(-50, 50)
end

function Ball:update(dt)
	self.x = self.x + self.dx * dt
	self.y = self.y + self.dy * dt
	hit_wall=false
	if self.x < 0  or (self.x > VIRTUAL_WIDTH) then
		--self.dx = (self.dx+math.random(-5,5)) * -1 
		self.dx = -self.dx
		hit_wall=true
	end
	if self.y < 0  or (self.y > VIRTUAL_HEIGHT) then
		--self.dy = (self.dy+math.random(-0.5,1.5)) * -1
		self.dy = -self.dy
		hit_wall=true
	end
	if self.y > VIRTUAL_HEIGHT - self.height then
		self.y = self.y - self.height / 2
		self.dy = -self.dy
	end
	return hit_wall
	
end
function Ball:collides(paddle)
	if self.x > paddle.x + paddle.width or paddle.x > self.x + self.width then
		return false
	elseif self.y > paddle.y + paddle.height or paddle.y > self.y + self.height then
		return false
	else
		ball.dy = math.floor(ball.dy * math.random(0.9,1.1))
		return true
	end
end
function Ball:draw()
	love.graphics.rectangle("fill",self.x,self.y,self.width,self.height)
end
