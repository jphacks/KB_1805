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

    input_file_path = @img_file[:tempfile].path
    res_file_path   = "./tmp/res.md"
    Convertor::convert(input_file_path, res_file_path)
    content_type Convertor.file_type(res_file_path)
    attachment res_file_path
    File.read(res_file_path)
  else
    @msg = "Error"
  end
end
