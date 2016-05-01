
my @size = qw/512/;
my @depth = qw/3/;
my @dropout = qw/0.8/;
my $maxEpoch = 2;
my @batchSize = qw/20/;
my @learningRate = qw/0.002/;
my @decay = qw/0.97/;
my @seq = qw/200/;
my @dats = qw/basic basicLineNo basicLineNoP basicP bi biLineNo biLineNoP biP   /;
my @inits = ("basic_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch50.00_0.1945.t7",
"basicLineNo_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.2649.t7",
"basicLineNoP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch0.23_0.0734.t7",
"basicP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch36.12_0.0142.t7",
"bi_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch68.09_0.1584.t7",
"biLineNo_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch29.33_0.1545.t7",
"biLineNoP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.0177.t7",
"biP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch6.16_0.0863.t7",
);
#my @dats = qw/basic basicP basicLineNo basicLineNoP bi biLineNo biLineNoP biP/;
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
			    print "th train.lua -rnn_size $s -num_layers $d -dropout $dr -seed 23 -learning_rate $lr -decay_rate $dc -seq_length $se -batch_size $b -max_epochs $maxEpoch -eval_val_every 1  -val_frac 1 -checkpoint_dir ${dat}_${s}_${d}_${dr}_${b}_${lr}_${dc}_${se} -data_dir data/${dat}Test -init_from $inits[$ind]\n";
			    system("th train.lua -rnn_size $s -num_layers $d -dropout $dr -seed 23 -learning_rate $lr -decay_rate $dc -seq_length $se -batch_size 1 -max_epochs $maxEpoch -eval_val_every 1  -train_frac 0.01 -val_frac .999 -checkpoint_dir ${dat}_${s}_${d}_${dr}_${b}_${lr}_${dc}_${se} -data_dir data/${dat}Test -init_from $inits[$ind]\n");
			}
		    }
		}
	    }
	}
    }
}
}
