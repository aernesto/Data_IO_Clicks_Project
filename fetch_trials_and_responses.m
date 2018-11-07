function [trials,responses]=fetch_trials_and_responses(filename,trial_range,shuffled,model_type)
% fetches both the trial and decision data within a specific range. Trial data contains click
% times, mainly, and decision data contains the choices from a single model (specified as arg).
% ARGS:
%   filename        full path to .h5 file
%   trial_range     1-by-2 vector describing a range of integers (endpoints
%                   included)
%   shuffled        boolean. If true, shuffles all trials in DB before
%                   returning the requested range. rng('shuffle') is called 
%                   inside this function.
%   model_type      one of 'lin' and 'nonlin'. Model responses are fetched from.
% RETURNS:
%   trials          3-by-N cell, where N=trial_range(2)-trial_range(1)+1. 
%                   First two rows of the cell contain click times for left
%                   and right streams. Third row contains change point 
%                   times. So, to access left and right click streams from
%                   trial M, as col vectors, type: 
%                   [left,right]=trials{1:2,M};
%   responses       1-by-N vector, where N=trial_range(2)-trial_range(1)+1. 
%                   Vector contains -1 at entry n whenever response
%                   on trial n was -1 (i.e. H-). +1 codes for H+.

% get metadata
file_info = h5info(filename);
group_name = file_info.Groups.Name;
trials_dset_name=[group_name,'/trials'];
trial_info = h5info(filename, trials_dset_name);
tot_num_trials = trial_info.Dataspace.Size(2);  % nb of trials in dataset
decision_dset_name=[group_name,'/decision_',model_type];

% fetch actual data
trials = h5read(filename,trials_dset_name);
responses=h5read(filename, decision_dset_name);


if tot_num_trials < trial_range(2) || trial_range(1)<1
    error('trial_range out of bounds')
elseif shuffled
    rng('shuffle')
    permutation=randperm(tot_num_trials);
    trials=trials(:,permutation);
    responses=responses(permutation);
end

trials=trials(:,trial_range(1):trial_range(2));
responses=responses(trial_range(1):trial_range(2));

end
