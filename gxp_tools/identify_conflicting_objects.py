#objects_from_untrusted = open("../gxp_outs/target_object_untrusted.out", 'r')
#objects_from_trusted =  open("../gxp_outs/target_object_trusted.out", 'r')

#for untrusted in objects_from_untrusted: 
	#print(untrusted)
#	for trusted in objects_from_trusted:
#		print(trusted)		
#		print(untrusted)
		#if (trusted == untrusted):
		#	print(trusted)

#print "done"clear


# STEP 1 - Get Target Object of trusted

obj_read = open("../gxp_outs/target_object_trusted.out", 'w')

stage = 0
skip = 0

with open('../gxp_outs/reads_by_trusted.out') as f:
        for line in f:
		for c in line:
			if c == ' ' and stage == 0:
				stage = 1
				continue
			elif c == ' ' and stage == 1 and skip == 0:
				stage = 2
				continue
			elif c == ' ' and stage == 3:
				stage = 4
				continue
			elif stage == 4:
				break						
			elif c == ':' and stage == 2:
				stage = 3
				obj_read.write(c)
				continue
			elif c == '{' and stage == 1 and skip == 0:
				skip = 1
			elif c == '}' and stage == 1 and skip == 1:
				skip = 0
			elif stage == 2:
				obj_read.write(c)
			elif c == '{' and stage == 3 and skip == 0:
				skip = 1
				obj_read.write(c)
			elif c == '}' and stage == 1 and skip == 1:
				skip = 0
				obj_read.write(c)
			elif stage == 3:
				obj_read.write(c)
				
		obj_read.write('\n')
		skip = 0
		stage = 0	

f.close()
obj_read.close()



# STEP 2 - Get Target Object of untrusted

obj_written = open("../gxp_outs/target_object_untrusted.out", 'w')

stage = 0
skip = 0

with open('../gxp_outs/writes_by_untrusted.out') as f:
        for line in f:
		for c in line:
			if c == ' ' and stage == 0:
				stage = 1
				continue
			elif c == ' ' and stage == 1 and skip == 0:
				stage = 2
				continue
			elif c == ' ' and stage == 3:
				stage = 4
				continue
			elif stage == 4:
				break						
			elif c == ':' and stage == 2:
				stage = 3
				obj_written.write(c)
				continue
			elif c == '{' and stage == 1 and skip == 0:
				skip = 1
			elif c == '}' and stage == 1 and skip == 1:
				skip = 0
			elif stage == 2:
				obj_written.write(c)
			elif c == '{' and stage == 3 and skip == 0:
				skip = 1
				obj_written.write(c)
			elif c == '}' and stage == 1 and skip == 1:
				skip = 0
				obj_written.write(c)
			elif stage == 3:
				obj_written.write(c)
				
		obj_written.write('\n')
		skip = 0
		stage = 0

f.close()
obj_written.close()




# STEP 3 - Identify Conflicting Objects

conflicts = open('../gxp_outs/conflicting_objects.out', 'w')
#neverallow = open('../../gxp_neverallow/neverallows.out', 'r') 

with open('../gxp_outs/target_object_untrusted.out', 'r') as file1:
    with open('../gxp_outs/target_object_trusted.out', 'r') as file2:
        same = set(file1).intersection(file2)

same.discard('\n')

#with open('some_output_file.txt', 'w') as file_out:
for obj in same:
	#print(obj)
	conflicts.write(obj)

	conflicts.write('\n')
	conflicts.write("\tWRITES BY UNTRUSTED: \n")
	with open('../gxp_outs/writes_by_untrusted.out') as f2:
		for line2 in f2:
			if obj.rstrip('\n') in line2:
				conflicts.write('\t' + line2)
	
	conflicts.write('\n')
	conflicts.write("\tREADS BY TRUSTED: \n")
	with open('../gxp_outs/reads_by_trusted.out') as f1:
		for line1 in f1:
			if obj.rstrip('\n') in line1:
				conflicts.write('\t' + line1)


	conflicts.write('\n')
	



# STEP 4 - Retrieve Neverallows for Conflicting Objects
	
	conflicts.write("\tNEVERALLOWS: \n")
	with open('../../gxp_neverallow/neverallows.out') as f3:
		for line3 in f3:
			if obj.rstrip('\n') in line3:
				conflicts.write('\t' + line3)


	conflicts.write('\n')

f1.close()
f2.close()
conflicts.close()

