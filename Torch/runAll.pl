

my @size = qw/512/;
my @depth = qw/3/;
my @dropout = qw/0.8/;
my $maxEpoch = 15;
my @batchSize = qw/20 50/;
my @learningRate = qw/0.002/;
my @decay = qw/0.97/;
my @seq = qw/200 300 400/;
my $dat = "smbBiPathsMk2";
foreach my $s (@size) {
    foreach my $d (@depth){ 
	foreach my $dr (@dropout){
	    foreach my $b (@batchSize) {
		foreach my $lr (@learningRate){
		    foreach my $dc (@decay){
			foreach my $se (@seq){
			    system("th train.lua -rnn_size $s -num_layers $d -dropout $dr -seed 23 -learning_rate $lr -decay_rate $dc -seq_length $se -batch_size $b -max_epochs $maxEpoch -eval_val_every 200 -val_frac 0.1 -checkpoint_dir ${dat}_${s}_${d}_${dr}_${b}_${lr}_${dc}_${se} -data_dir data/$dat \n");
			    system("th train.lua -rnn_size $s -num_layers $d -dropout $dr -seed 6546 -learning_rate $lr -decay_rate $dc -seq_length $se -batch_size $b -max_epochs $maxEpoch -eval_val_every 200 -val_frac 0.1 -checkpoint_dir ${dat}_${s}_${d}_${dr}_${b}_${lr}_${dc}_${se} -data_dir data/$dat \n");
			}
		    }
		}
	    }
	}
    }
}
