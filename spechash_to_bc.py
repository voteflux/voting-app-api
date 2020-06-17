from update_ballotspecs_db import update_ballotspecs, render_spec_hash

print(render_spec_hash("test"))
update_ballotspecs("t1234", "test short title", "test question",
                    "test description", "test start date", "testber", "test sponsor")

