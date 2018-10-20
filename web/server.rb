require 'bundler/setup'
require 'sinatra'
require 'haml'

require 'fileutils'
require 'securerandom'

require_relative './convertor.rb'

get "/" do
  haml :index
end

post "/upload" do
  if params[:file]
    @img_file = params[:file]

    p "#{@img_file}"
    uuid = SecureRandom.uuid

    input_file_path = @img_file[:tempfile].path
    @res_file_path  = File.join("tmp", "#{uuid}.md")

    Convertor::convert(input_file_path, @res_file_path)
    content_type Convertor.file_type(@res_file_path)

    input_file_name = @img_file[:filename]
    attachment_name = File.basename(input_file_name, File.extname(input_file_name))
    attachment "#{attachment_name}.md"
    File.read(@res_file_path)

    STDERR.puts "#{attachment_name}.md"
  else
    @msg = "Error"
  end
end

after "/upload" do
  if @res_file_path && Dir[@res_file_path]
    FileUtils.rm_rf(@res_file_path)
  end
end
