# This code was made entirely using DeepSeek Coder.
# Link to the model: https://huggingface.co/collections/deepseek-ai/deepseek-coder


import sys
import types

def create_dummy_torch_cuda():
    if 'torch.cuda' in sys.modules:
        return
    try:
        import torch.cuda
        return
    except ImportError:
        pass

    dummy = types.ModuleType('torch.cuda')
    dummy.is_available = lambda: False
    dummy.device_count = lambda: 0
    dummy.current_device = lambda: 0
    dummy.get_device_name = lambda *args, **kwargs: 'dummy'
    dummy.Stream = type('Stream', (), {})
    dummy.Event = type('Event', (), {})
    dummy.synchronize = lambda *args, **kwargs: None
    dummy.manual_seed = lambda *args, **kwargs: None
    dummy.manual_seed_all = lambda *args, **kwargs: None
    dummy.init = lambda *args, **kwargs: None
    dummy.empty_cache = lambda *args, **kwargs: None
    dummy.memory_allocated = lambda *args, **kwargs: 0
    dummy.memory_reserved = lambda *args, **kwargs: 0
    dummy.max_memory_allocated = lambda *args, **kwargs: 0
    dummy.max_memory_reserved = lambda *args, **kwargs: 0
    dummy.get_arch_list = lambda *args, **kwargs: []
    dummy.get_device_capability = lambda *args, **kwargs: (0, 0)
    dummy.get_device_properties = lambda *args, **kwargs: type('Props', (), {'name': 'dummy'})()
    dummy.set_device = lambda *args, **kwargs: None
    dummy.device = lambda *args, **kwargs: None
    dummy.device_of = lambda *args, **kwargs: None
    dummy.ipc_collect = lambda *args, **kwargs: None
    dummy.utilization = lambda *args, **kwargs: 0
    dummy.clock_rate = lambda *args, **kwargs: 0
    dummy.pci_bus_id = lambda *args, **kwargs: '0000:00:00.0'
    dummy.memory_stats = lambda *args, **kwargs: {}
    dummy.memory_summary = lambda *args, **kwargs: ''
    dummy.memory_snapshot = lambda *args, **kwargs: []
    dummy.reset_peak_memory_stats = lambda *args, **kwargs: None
    dummy.reset_accumulated_memory_stats = lambda *args, **kwargs: None
    dummy.list_gpus = lambda *args, **kwargs: []
    dummy.get_rng_state = lambda *args, **kwargs: None
    dummy.get_rng_state_all = lambda *args, **kwargs: []
    dummy.set_rng_state = lambda *args, **kwargs: None
    dummy.set_rng_state_all = lambda *args, **kwargs: None
    dummy.initial_seed = lambda *args, **kwargs: 0
    dummy.seed = lambda *args, **kwargs: None
    dummy.seed_all = lambda *args, **kwargs: None
    dummy.is_initialized = lambda: False
    dummy.cudart = None
    dummy.nvrtc = None
    dummy.cudnn = None
    dummy.cufft = None
    dummy.curand = None
    dummy.cusolver = None
    dummy.cusparse = None
    dummy.nvtx = None
    dummy.driver = None
    dummy.graphs = None
    dummy.green_contexts = None
    dummy.jiterator = None
    dummy.lazy_init = lambda: None
    dummy._lazy_init = lambda: None
    dummy._initialized = False
    dummy._tls = None

    sys.modules['torch.cuda'] = dummy
    try:
        import torch
        torch.cuda = dummy
    except ImportError:
        pass

create_dummy_torch_cuda()