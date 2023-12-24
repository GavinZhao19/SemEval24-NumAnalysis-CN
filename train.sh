export PDSH_RCMD_TYPE=ssh
export NCCL_IB_DISABLE=0
export NCCL_DEBUG=INFO
export NCCL_SOCKET_IFNAME=eth0
export NCCL_IB_GID_INDEX=3
export NCCL_IB_TC=184
export NCCL_IB_RETRY_CNT=7
export NCCL_IB_TIMEOUT=23
export NCCL_NET_GDR_LEVEL=1
export NCCL_IB_PCI_RELAXED_ORDERING=1
export NCCL_IB_HCA=mlx5_0,mlx5_1,mlx5_2,mlx5_3
export NCCL_ALGO=Ring
export NCCL_NET_GDR_READ=1
export UCX_IB_PCI_RELAXED_ORDERING=on
CUDA_VISIBLE_DEVICES="0,1,2,3,4,5,6,7" accelerate launch --config_file platform_default_config.yaml.multi.2machine src/train_bash.py \
    --stage sft \
    --template chatglm3 \
    --model_name_or_path /root/.cache/huggingface/hub/models--THUDM--chatglm3-6b/snapshots/fc3235f807ef5527af598c05f04f2ffd17f48bab \
    --do_train \
    --dataset_dir data/group_chat/sft_semval/rawdata \
    --token_cache_dir data/group_chat/sft_semval/cache \
    --finetuning_type full \
    --max_source_length 2048 \
    --max_target_length 2048 \
    --output_dir output/sft-semval-chatglm3-6B\
    --overwrite_cache \
    --per_device_train_batch_size 2 \
    --per_device_eval_batch_size 2 \
    --gradient_accumulation_steps 1 \
    --evaluation_strategy "steps" \
    --eval_steps 500 \
    --save_strategy "steps" \
    --save_steps 500 \
    --warmup_ratio 0.01 \
    --lr_scheduler_type cosine \
    --logging_steps 5 \
    --learning_rate 1e-6 \
    --num_train_epochs 10.0 \
    --preprocessing_num_workers 64 \
    --plot_loss \
    --fp16 True \
    --overwrite_output_dir True \
    --batch_tokenize True \
    --max_token_batch 500000 \
    --dataset train \
    --eval_dataset valid \