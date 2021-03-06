function trials=fetch_trials(filename,trial_range,shuffled)
% ARGS:
%   filename        full path to .h5 file
%   trial_range     1-by-2 vector describing a range of integers (endpoints
%                   included)
%   shuffled        boolean. If true, shuffles all trials in DB before
%                   returning the requested range. rng('shuffle') is called 
%                   inside this function.
% RETURNS:
%   trials          3-by-N cell, where N=trial_range(2)-trial_range(1)+1. 
%                   First two rows of the cell contain click times for left
%                   and right streams. Third row contains change point 
%                   times. So, to access left and right click streams from
%                   trial M, as col vectors, type: 
%                   [left,right]=trials{1:2,M};

% get metadata
file_info = h5info(filename);
group_name = file_info.Groups.Name;
trials_dset_name=[group_name,'/trials'];
trial_info = h5info(filename, trials_dset_name);
tot_num_trials = trial_info.Dataspace.Size(2);  % nb of trials in dataset

% fetch actual data
trials = h5read(filename,trials_dset_name);

if tot_num_trials < trial_range(2) || trial_range(1)<1
    error('trial_range out of bounds')
elseif shuffled
    rng('shuffle')
    trials=trials(:,randperm(tot_num_trials));
end

trials=trials(:,trial_range(1):trial_range(2));
end