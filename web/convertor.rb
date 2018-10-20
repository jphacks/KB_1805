require "bundler/setup"
require "ruby-filemagic"

module Convertor
  SUPPORTED_FILE_TYPES = ["image/jpeg", "image/png"]

  class << self
    def file_type(file_path)
      FileMagic.new(FileMagic::MAGIC_MIME).file(file_path).split(";").first
    end

    def image?(file_path)
      SUPPORTED_FILE_TYPES.include?(file_type(file_path))
    end

    def convert(input_path, output_path)
      STDERR.puts "Start converting the file '#{input_path}'"
      `python ./tool/img2md.py #{input_path} #{output_path}`
    end

    def compress_zip(dir_path)
    end
  end
end
