provider "aws" {
  region = "eu-central-1" # Frankfurt régió (közel van, gyors)
}

# Tűzfal beállítások: Engedélyezzük a 8000-es portot az API-nak és a 22-est az SSH-nak
resource "aws_security_group" "api_sg" {
  name        = "books_api_sg_v2"
  description = "Allow HTTP and SSH traffic"

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Maga a virtuális szerver (Ingyenes t3.micro)
resource "aws_instance" "api_server" {
  ami           = "ami-04e601abe3e1a910f" # Ubuntu 22.04 LTS
  instance_type = "t3.micro"
  vpc_security_group_ids = [aws_security_group.api_sg.id]

  # Ez a szkript lefut a szerver indulásakor: telepít, adatot gyűjt és API-t indít
  user_data = <<-EOF
              #!/bin/bash
              sudo apt-get update
              sudo apt-get install -y python3-pip python3-venv git
              
              cd /home/ubuntu
              git clone https://github.com/spawn187/books-scraper-api.git
              cd books-scraper-api
              
              python3 -m venv venv
              source venv/bin/activate
              pip install -r requirements.txt
              
              # Scraper futtatása az adatbázis feltöltéséhez
              python3 scraper.py
              
              # API szerver elindítása a háttérben
              nohup uvicorn main:app --host 0.0.0.0 --port 8000 > api.log 2>&1 &
              EOF

  tags = {
    Name = "BooksScraperAPI"
  }
}

# Kiíratjuk a szerver IP címét a végén
output "api_public_ip" {
  value = aws_instance.api_server.public_ip
}