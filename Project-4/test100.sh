date
for topo in HundredRandomGeneratedTopos/*Topo.txt
do
        topo=$(basename $topo .txt)
        echo $topo ---
        python run_topo.py HundredRandomGeneratedTopos/${topo}.txt /tmp/out.log > /dev/null
        lines=$(wc -l < HundredRandomGeneratedTopos/${topo}.log)
        sed '$d' /tmp/out.log | tail -$(echo $lines) | diff HundredRandomGeneratedTopos/${topo}.log -
done
date