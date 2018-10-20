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

    def convert(file_path)
      STDERR.puts "Start converting the file '#{file_path}'"
    end
  end
end
