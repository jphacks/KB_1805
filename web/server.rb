require 'bundler/setup'
require 'sinatra'
require 'haml'

require 'fileutils'
require 'securerandom'

require_relative './convertor.rb'
require_relative './compress.rb'

get "/" do
  haml :index
end

post "/upload" do
  if params[:file]
    @img_file = params[:file]

    p "#{@img_file}"
    uuid = SecureRandom.uuid

    input_file_path = @img_file[:tempfile].path
    @res_dir_path   = File.join("tmp", "#{uuid}")
    @res_zip_path   = File.join("tmp", "#{uuid}.zip")
    Convertor::convert(input_file_path, @res_dir_path)
    # @res_dir_path   = File.join("tmp", "test")
    # @res_zip_path   = File.join("tmp", "test.zip")

    zf = ZipFileGenerator.new(@res_dir_path, @res_zip_path)
    zf.write

    input_file_name = @img_file[:filename]
    attachment_name = File.basename(input_file_name, File.extname(input_file_name))

    content_type Convertor.file_type(@res_dir_path)
    attachment "#{attachment_name}.zip"
    File.read(@res_zip_path)
  else
    @msg = "Error"
  end
end

after "/upload" do
  if @res_dir_path && Dir[@res_dir_path]
    FileUtils.rm_rf(@res_dir_path)
    FileUtils.rm_rf(@res_zip_path)
  end
end
