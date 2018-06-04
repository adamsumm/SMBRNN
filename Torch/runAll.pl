

my @size = qw/2048/;
my @depth = qw/3/;
my @dropout = qw/0.95/;
#my @maxEpoch = qw/100 20 50 10 50 10 10 10/; 
my @maxEpoch = qw/400/; 
my @batchSize = qw/32/;
my @learningRate = qw/0.002/;
my @decay = qw/0.97/;
my @seq = qw/200/;
my @dats = qw/metroid_againstGrain_paths metroid_againstGrain/; 
my @inits = ("","","","","","","","","","","","","","","","","","","","","","","",);

my $ind = -1;
foreach my $dat (@dats){
    $ind++;
foreach my $s (@size) {
    foreach my $d (@depth){ 
	foreach my $dr (@dropout){
	    foreach my $b (@batchSize) {
		foreach my $lr (@learningRate){
		    foreach my $dc (@decay){
			foreach my $se (@seq){
				    #$ba = int(300.0/(1.0*$maxEpoch[$ind]));
				    $ba = $b;
			    print "Running th train.lua -rnn_size $s -num_layers $d -dropout $dr -seed 23 -learning_rate $lr -decay_rate $dc -seq_length $se -batch_size $ba -max_epochs $maxEpoch[$ind] -eval_val_every 1000 -val_frac 0.1 -checkpoint_dir ${dat}_${s}_${d}_${dr}_${b}_${lr}_${dc}_${se} -data_dir data/$dat $inits[$ind]\n";
			    system("th train.lua -rnn_size $s -num_layers $d -dropout $dr -seed 23 -learning_rate $lr -decay_rate $dc -seq_length $se -batch_size $ba -max_epochs $maxEpoch[$ind] -eval_val_every 1000 -val_frac 0.1 -checkpoint_dir ${dat}_${s}_${d}_${dr}_${b}_${lr}_${dc}_${se} -data_dir data/$dat $inits[$ind]\n");
			}
		    }
		}
	    }
	}
    }
}
}
