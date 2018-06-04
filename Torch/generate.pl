

my @networks = qw{
biLineNoP_512_3_0.8_20_0.002_0.97_200/lm_lstm_epoch20.00_0.0177.t7
};

my @folders = qw{
biLineNoP_512_3_0.8};

my @regular_texts = qw{
;(-------------XXX)XXX-------------(------------*XXX 
;(-------------XXX)XXX-------------(------------*XXX 
;(-------------XXX)XXX-------------(------------*XXX 
;(-------------XXX)XXX-------------(------------*XXX 
;(-------------XXX)XXX-------------(------------*XXX };


my $start = 11929;
my $samples = 100000;
for my $network (@networks){
    system("mkdir output$folders[$ind]");   
    for my $seed ($start..($start+$samples-1)){
	print "Running 'th sample.lua $network -primetext  \";(-------------XXX)XXX-------------(------------*XXX)\" -seed $seed -length 8000 > output$folders[$ind]/raw.$seed'\n";
	system("th sample.lua $network  -primetext  \";(-------------XXX)XXX-------------(------------*XXX)\" -temperature 1.0 -seed $seed -length 8000 > output$folders[$ind]/rawAG.$seed ");

    }
    $ind++;
}
