require 'bundler/setup'
require 'sinatra'
require 'haml'

require 'fileutils'

require_relative './convertor.rb'

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

    # Convertor::convert(@img_file[:filename])
    res_file_path = "./tmp/blank.md"
    content_type Convertor.file_type(res_file_path)
    attachment res_file_path
    File.read(res_file_path)
  else
    @msg = "Error"
  end
end
