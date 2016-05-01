

my @size = qw/512/;
my @depth = qw/3/;
my @dropout = qw/0.8/;
#my @maxEpoch = qw/100 20 50 10 50 10 10 10/; 
my @maxEpoch = qw/30 30/; 
my @batchSize = qw/300/;
my @learningRate = qw/0.002/;
my @decay = qw/0.97/;
my @seq = qw/200/;
my @dats = qw/basicP/; 
#my @dats = qw/basic basicP basicLineNo basicLineNoP bi biLineNo biLineNoP biP/; #qw/basic   /;
my @inits = ("-init_from  basicP_512_3_0.8_300_0.002_0.97_200/lm_lstm_epoch5.02_0.0980.t7","-init_from biLineNo_512_3_0.8_300_0.002_0.97_200/lm_lstm_epoch21.05_0.1269.t7","-init_from basicLineNo_512_3_0.8_300_0.002_0.97_200/lm_lstm_epoch50.00_0.1392.t7","","","","","","","","","","","","","","","","","","","","","","","",); #( "-init_from biLineNoP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch2.21_0.0997.t7","","","","","","","","","","","","","","","","",);
#my @dats = qw/ biLineNoP biP/; # qw/basic basicP basicLineNo basicLineNoP bi biLineNo biLineNoP biP/;
#my @inits = ( "-init_from basic_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.3499.t7",
#	      "-init_from basicP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.0291.t7",
#	      "-init_from basicLineNo_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.2649.t7",
#	      "-init_from basicLineNoP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch7.04_0.0765.t7",
#	      "-init_from bi_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.2907.t7",
#	      "-init_from biLineNo_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.1746.t7",
#	      "-init_from biLineNoP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.0177.t7",
#	      "");
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
			    $ba = int(300.0/(1.0*$maxEpoch[$ind]));
			    print "Running th train.lua -rnn_size $s -num_layers $d -dropout $dr -seed 23 -learning_rate $lr -decay_rate $dc -seq_length $se -batch_size $ba -max_epochs $maxEpoch[$ind] -eval_val_every 200 -val_frac 0.1 -checkpoint_dir ${dat}_${s}_${d}_${dr}_${b}_${lr}_${dc}_${se} -data_dir data/$dat $inits[$ind]\n";
			    system("th train.lua -rnn_size $s -num_layers $d -dropout $dr -seed 23 -learning_rate $lr -decay_rate $dc -seq_length $se -batch_size $ba -max_epochs $maxEpoch[$ind] -eval_val_every 200 -val_frac 0.1 -checkpoint_dir ${dat}_${s}_${d}_${dr}_${b}_${lr}_${dc}_${se} -data_dir data/$dat $inits[$ind]\n");
			}
		    }
		}
	    }
	}
    }
}
}
