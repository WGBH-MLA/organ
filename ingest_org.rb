DAHOST = "localhost:8000"
[File.read("orgs.csv").split("\n")[1]].each do |org|
  title,short_name,city,state_abbreviation,url,about_html,logo_src,productions_html = org.split(",")
  puts "now ingesting #{title}"
  resp = `curl -X POST #{DAHOST}/org -d 'name=#{title}&short_name=#{short_name}&city=#{city}&state=#{state_abbreviation}&url=#{url}&about=#{about_html}&logo_url=#{logo_src}&productions=#{productions_html}'`

  puts "done!"
end
