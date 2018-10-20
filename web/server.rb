require 'bundler/setup'
require 'sinatra'
require 'haml'

get "/" do
  haml :index
end

post "/upload" do
  if params[:file]
    @img_file = params[:file]

    p "#{@img_file}"

    save_path = "./tmp.png"
    File.open(save_path, 'wb') do |f|
      f.write @img_file[:tempfile].read
    end

    @msg = "The image has succesfully uploaded"
  else
    @msg = "Error"
  end
end
